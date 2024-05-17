import base64
from io import BytesIO
import re
import secrets

import pyotp
import qrcode
import requests
from ppss_auth.ppss_auth_utils.emailclient import sendConfirmEmailUseCase, sendPasswordResetEmailUseCase
from ppss_auth.ppss_auth_utils.password import getPasswordDigest

from pyramid.request import Request
from pyramid.response import Response
from pyramid.authentication import AuthTktCookieHelper
from pyramid.settings import asbool
from pyramid.renderers import render_to_response

from ..constants import Conf
from ..ppss_auth_utils import checkPassword,_,__
from ..models import PPSsResetTokens, PPSsuser,PPSsgroup,PPSspermission,PPSsloginhistory,constants

from pyramid.view import view_defaults,view_config,forbidden_view_config
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from beaker.cache import cache_region
from sqlalchemy.exc import InvalidRequestError



import os,datetime,logging
from datetime import timedelta
l = logging.getLogger('ppssauth')


from pyramid.security import (
    Everyone, Authenticated,
    remember,forget,
    Allow,Deny,
    Everyone,ALL_PERMISSIONS
    )


def getPrincipals(uid,request):
    groups = request.session.get('principals',[])
    l.debug("####  usergroups:{g}".format(g=groups))
    return groups

#this class build the ACL consumed by ACLRoot
#ACL is in the form: {group name: [list of permission names]} and is derived by ppss_groups and ppss_permission)
#permissions to be used in views are ppss_permission elements.
class ACLBuilder(object):
    def __init__(self,baseACL,dbsession):
        self.baseACL = baseACL
        self.session  = dbsession

    @cache_region('short_term', 'ACLpermissions')
    def buildACL(self):
        l.debug("buildACL cache miss")
        acl = [] 
        try:
            groups = self.session.query(PPSsgroup).filter(PPSsgroup.enabled==1).all()
            for group in groups:
                acl.append( (Allow,
                        str("g:"+group.name),
                        tuple([str(p.name) for p in group.permissions])  
                ) )
        except InvalidRequestError as invalid_session:
            l.exception("**************invalid_session. Something is going very very wrong!!")
            #raise invalid_session
        except Exception as e:
            l.warn("called without a transaction")
        acl = self.baseACL + acl
        l.info("ACLBuilder:acl built: {acl}".format(acl = acl))
        return acl


#This class stores the acl structure used by the root factory
class ACLRoot(object):
    baseACL=[(Allow, Authenticated, 'view'),
        (Allow, 'g:'+constants.SYSADMINGROUP, ALL_PERMISSIONS),
        (Allow, 'ppss_auth:changepassword',"ppss_auth_changepassword"),
        (Allow, 'ppss_auth:otpverify',"ppss_auth_otpverify")
        ]

    lastupdateACL = datetime.datetime.now()
    __acl__ = [
        (Allow, 'g:'+constants.SYSADMINPERM, ALL_PERMISSIONS)
    ]


    def __init__(self, request):
        self.request = request
        aclb = ACLBuilder(ACLRoot.baseACL,request.dbsession)
        ACLRoot.__acl__ = aclb.buildACL()


class ForbiddenRoute():
    def __init__(self,request):
        self.request = request

    #@view_config(route_name='ppsslogin',request_method="GET",renderer=Conf.logintemplate)
    def login(self):
        authcontroller = AuthController(self.request)
        return authcontroller.login()


@view_defaults(require_csrf=True)
class AuthController():

    def getUserById(self,userid):
        if userid<0:
            user = PPSsuser()
        else:
            user = PPSsuser.byId(userid,self.request.dbsession)
        return user

    def isCaptchaEnabled(self) -> bool:
        if Conf.turnstile_sitekey and Conf.turnstile_secretkey:
            return True
        else:
            return False
        
    def verifyCaptcha(self,token) -> bool:
        try:
            r = requests.post('https://challenges.cloudflare.com/turnstile/v0/siteverify', data={
                'secret': Conf.turnstile_secretkey,
                'response': token
            })
            r.raise_for_status()
            return r.json()['success']
        except Exception as e:
            l.exception("Captcha api call failed")
            return False

    def __init__(self,request:Request):
        request.response.headers["X-Frame-Options"] = "DENY"
        request.response.headers["Content-Security-Policy"] = "frame-ancestors 'none';"
        self.request = request
        self.user = None
        activemenu = ""
        activeaction = ""
        ##request.bt = Conf['bootstrapclasses']

        try:
            mr = self.request.matched_route.name.split(":")
            if len(mr) == 3:
                activemenu = mr[1]
                activeaction = mr[2]
        except:
            pass

        #for all ops on users, get the target user
        self.userid = int(
            self.request.params.get("userid",
                self.request.matchdict.get("elementid",
                    self.request.session[Conf.sessionuser]['id'] if Conf.sessionuser in self.request.session else -1 ) 
                )
            )
        self.user = self.getUserById(self.userid)
        

        self.retdict = {
            'midtpl':Conf.sectiontemplateinherit,
            'supertpl':Conf.mastertemplateinherit,
            'botplinherit':Conf.botemplateinherit,
            'logintpl': Conf.publictemplateinherit,
            'activemenu' : activemenu,
            'activeaction' : activeaction,
            'bc': Conf.bootstrapClasses,
            'ppsauthconf':Conf,
            'msg':"",
            'isCaptchaEnabled': self.isCaptchaEnabled(),
        }

    def logloginattempt(self,user,validity,username):
        self.request.dbsession.add(
                PPSsloginhistory(
                    user_id = user.id if user else None,
                    ipaddress = self.request.remote_addr,
                    result = validity.result(),
                    resultreason = validity.resultreason(),
                    username = username
                )
            )
        l.info("login attempt for user '{username}' result is '{result}':{enter}".format(username=username,result = validity.resultreason(),enter="OK" if validity else "Denied" ) )


    @view_config(route_name='ppsslogin',renderer=Conf.logintemplate)
    def login(self):
        r = self.request
        postloginpage = self.request.referer if (self.request.referer and self.request.referer!=self.request.route_url("ppsslogin")) else r.route_url(Conf.postloginroute)
        l.info("postloginpage = {},referer = {}, loginurl = {}, plr = {}, is true? {}".format(
            postloginpage, 
            self.request.referer, 
            self.request.route_url("ppsslogin"),
            r.route_url(Conf.postloginroute), (self.request.referer and self.request.referer!=self.request.route_url("ppsslogin")) )   )
        if self.request.referer:
            if self.request.loggeduser:
                signinreason = "Your current account has insufficent rights to view the page you requested.</br>You can change the account you are using with a new login."
            else:
                signinreason = "Please login to view the requested content."
        else:
            signinreason = ""
        self.retdict["signinreason"] = signinreason

        self.retdict["email_is_required"] = Conf.email_is_required

        self.request.session['postloginpage'] = postloginpage
        if self.user and self.user.passwordExpired():
            return HTTPFound(r.route_url("ppss:user:changepassword"))

        if r.POST:
            username = r.params.get("username",u"")
            password = r.params.get("password",u"")
            if self.isCaptchaEnabled():
                captcha = r.params.get("cf-turnstile-response",u"")
                if not captcha:
                    self.retdict["msg"] = "Captcha is required."
                    return self.retdict
                if self.verifyCaptcha(captcha) == False:
                    self.retdict["msg"] = "Captcha verification failed."
                    return self.retdict
            superuser = False
            res = None
            l.info("Login attempt: u={username}".format(username=username))
            if res is None:
                res,valid = PPSsuser.checkLogin(username,password,r.dbsession,ipaddr = self.request.remote_addr)
                self.logloginattempt(res,valid,username)
            if res and valid:
                res.getPermissionsMap()
                sessionvals = self.getSessionVals(self.setPrincipalsInSession(res,superuser,res.passwordExpired(), res.is2faEnabled()))                
                r.dbsession.expunge(res)
                l.info(f"session keys:{sessionvals}")


                ## log the last login
                llogin = PPSsuser.byId(res.id,r.dbsession)
                llogin.lastlogin = datetime.datetime.now()  
                l.debug("last login:{}".format(llogin.lastlogin))
                r.session.invalidate()
                
                r.session.update(sessionvals)                
                r.session[Conf.sessionuser] = {'id':res.id,'name':username,'user':res}
                headers = remember(r, res.id)
                r.session.save()
                if res.passwordExpired(): 
                    return HTTPFound(r.route_url("ppss:user:changepassword"))
                if res.is2faEnabled():
                    return HTTPFound(r.route_url("ppss:user:verifyotp"))
                return HTTPFound(postloginpage,headers=headers)
            #wrong password or disabled user
            
            l.warn("Login attempt failed for user {user}".format(user=username))
            if valid.blocked():
                msgorig = _('Your account seems to be temporarly blocked. Please wait before retrying or contact your adminstrator.')
            else:
                msgorig = _('something went wrong with your login. Please check your informations')
            msg = r.localizer.translate(msgorig,domain="ppss_auth")
            l.info("message is {} with locale '{}' and domain {}".format(msg,r.localizer.locale_name,msgorig.domain))
            self.retdict.update({'logintpl': Conf.publictemplateinherit ,'msg':msg})
            return self.retdict
        self.retdict.update({'logintpl': Conf.publictemplateinherit , 'msg':''})
        return self.retdict
    
    @view_config(route_name='ppss:user:verifyotp', permission='ppss_auth_otpverify', renderer=Conf.verify2fatpl)
    def verify_otp(self):
        if self.request.POST:
            otp = self.request.POST.get('otp', None)
            if otp:
                otp = int(otp)
                is_otp_valid = self.isOtpValid(otp=otp, otp_hash=self.user.otp_hash)
                if is_otp_valid:
                    postloginpage = self.request.session['postloginpage']
                    self.assign_user_perm(user=self.user)
                    
                    return HTTPFound(postloginpage)

            self.retdict['msg'] = __(self.request,'Something went wrong... please retry')
            return self.retdict 
        return self.retdict
    
    def assign_user_perm(self, user):
        r = self.request
        superuser = False
        user.getPermissionsMap()
        sessionvals = self.getSessionVals(self.setPrincipalsInSession(user,superuser,user.passwordExpired()))                
        r.dbsession.expunge(user)
        l.info(f"session keys:{sessionvals}")
        r.session.update(sessionvals)


    @view_config(route_name='ppsslogout')
    def logout(self):
        l.debug("logout")
        l.debug("principals = {pr}".format(pr=self.request.session.get('principals',[])  ))

        headers = forget(self.request)
        self.request.session.pop('admin',None)
        self.request.session.pop(Conf.sessionuser,None)
        self.request.session.pop('principals',None)
        
        return HTTPFound(self.request.route_url(Conf.postlogoutroute),headers=headers)

    def oauthCallBack(self):
        return Response("OK")

    def registernewuser(self):
        if not Conf.usercanregister:
            HTTPFound(self.request.route_url('ppsslogin'))
        retdict = self.retdict
        retdict["link"] = ["",""]
        retdict["email_is_required"] = Conf.email_is_required
        if self.request.POST:
            cancreate = True
            username = self.request.params.get("username","")
            password = self.request.params.get("password","")
            confirmnewpassword = self.request.params.get("confirmnewpassword","")
            email = self.request.params.get("email",None)
            if Conf.email_is_required:
                if not email:
                    retdict['msg'] += __( self.request,"Email is required")
                    cancreate = False
                if not email_is_valid(email):
                    retdict['msg'] += __( self.request,"Email is invalid")
                    cancreate = False
            if (email != ""):
                if len(PPSsuser.byField("email",email,self.request.dbsession))>0:
                        retdict['msg'] += "Email '{}' already used.".format(email)
                        cancreate = False
            
            if not username:
                retdict["msg"] +=__(self.request,"Username can not be empty.")
                cancreate = False
            if not password:
                retdict["msg"] +=__(self.request,"Password can not be empty.")
                cancreate = False
            if password != confirmnewpassword:
                retdict["msg"] +=__(self.request,"Password check doesn't match the password.")
                cancreate = False
            chkres = checkPassword(PPSsuser(username=username),password)
            if not chkres:
                retdict["msg"] += chkres.getMsg(self.request)
                #__(self.request,"Password doesn't respect minimum constraints.")
                cancreate = False
            if cancreate:
                # user = PPSsuser(username = username, newemail=email, newemailmagic=uuid4(), enabled=-1)
                enabled = -1 if Conf.email_is_required else 1
                user = PPSsuser(username = username, enabled=enabled)
                user.setPassword(password)
                for g in Conf.newusergroups:
                    group = PPSsgroup.byName(g,self.request.dbsession)
                    if group:
                        user.groups.append(group)
                self.request.dbsession.add(user)

                # email verify
                token = secrets.token_urlsafe()
                hashed_token = getPasswordDigest(token)
                user_token = PPSsResetTokens(token=hashed_token, reset_type='email', additionaldata=email,  token_expiry=datetime.datetime.now() + timedelta(days = 7))
                user.tokens.append(user_token)
                sendConfirmEmailUseCase(request=self.request).run(user=user, email=email, token=token)
                
                
                if Conf.email_is_required:
                    retdict['msg'] = __(self.request,"Please check your email for activation link.")
                else:
                    retdict['msg'] = __(self.request,"User created, please go to login page.")
                    
                retdict["link"] = ["login",self.request.route_url("ppsslogin")]
            
            # HTTPFound(self.request.route_url("ppsslogin"))
        return retdict
        
    @view_config(route_name="ppss:user:changepassword",renderer=Conf.changepasswordtemplate,permission='ppss_auth_changepassword')
    def ppsschangepassword(self):
        l.debug("change password")
        if not Conf.sessionuser in self.request.session:
            return HTTPFound(self.request.route_url("ppsslogin"))
        message = ""
        forcedtochange=False
        if self.user.passwordExpired():
            #dead code here, message never used
            message = Conf.passwordexpiredmessage
            forcedtochange=True
        
        retdict = {'logintpl': Conf.publictemplateinherit,'msg':message,'res':True}
        retdict.update(self.retdict)
        if self.request.POST:
            oldpassword = self.request.params.get("oldpassword")
            newpassword = self.request.params.get("newpassword")
            confirmnewpassword = self.request.params.get("confirmnewpassword","")
            if newpassword!=confirmnewpassword:
                retdict['res']=False
                retdict['msg']=__(self.request,"Password check doesn't match the password.")
                return retdict
            username = self.request.session.get(Conf.sessionuser).get("name")
            user,valid = PPSsuser.checkLogin(username,oldpassword,self.request.dbsession)     

            if valid:
                res = checkPassword(user,newpassword)
                l.info("checkPassword result for user {} = {}".format(user.username, res.getMsg(self.request) ))
                if res:
                    user.setPassword(newpassword)
                    retdict['msg'] = __(self.request,"Password updated.")
                    l.info("password upadated for user '{}'".format(user.username))
                    if forcedtochange:
                        #load permission for user forced to change password
                        self.setPrincipalsInSession(user,user.isSuperUser(),False   )
                else:
                    retdict['res']=False
                    retdict['msg'] = res.getMsg(self.request)
                    #__(self.request,"New password doesn't match constraints." )
                    l.info("password upadated failed for user '{}'".format(user.username))
            else:
                retdict['res']=False
                retdict['msg']=__(self.request,'Old password is wrong')
        return retdict
        
    def setPrincipalsInSession(self,user:PPSsuser,isSuperUser=None,passwordExpired=None, is2faEnabled=None):
        if isSuperUser  is None:
            isSuperUser = user.isSuperUser()
        if passwordExpired is None:
            passwordExpired  = user.passwordExpired()
        r = self.request
        if isSuperUser:
            r.session['admin'] = True
            r.session['principals'] = ["g:admin","g:sysadmin"]
        else:
            r.session['principals'] = user.getPrincipals(passwordExpired, is2faEnabled) 
            r.session['admin'] = False
        l.info("permissions for {}({},{}):{}".format(user.username,isSuperUser,passwordExpired,r.session['principals'])  )
        r.session.changed()
        return r.session

    def getSessionVals(self,session,all=False):
        allvals = {k:session.get(k) for k in session.keys() if (not k.startswith("_")) or all }
        l.debug(f"all session vals:{allvals}")
        return allvals

    def listUser(self):
        elements = self.request.dbsession.query(PPSsuser).all()
        retdict = {'elements':elements}
        retdict.update(self.retdict)
        return retdict
    
    @view_config(route_name='2fa:enable',request_method='GET',  renderer=Conf.enable2fatpl)
    def enable_2fa_get(self):
        if self.user and self.user.otp_hash:
            self.retdict['errmsg'] =__(self.request,'2fa already activated')
            return self.retdict
        otp_hash = pyotp.random_base32()
        self.retdict['img_str'] = self.qrcode_img_from_otp_hash(otp_hash=otp_hash)
        self.retdict['otp_hash'] = otp_hash
        
        return self.retdict
    
    def qrcode_img_from_otp_hash(self, otp_hash) -> str:
        uri = pyotp.totp.TOTP(otp_hash).provisioning_uri(self.user.username,issuer_name=Conf.issuer2fa)
        image = qrcode.make(uri)
        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()) 
        img_base64 = bytes("data:image/jpeg;base64,", encoding='utf-8') + img_str
        img_base64_str = img_base64.decode("utf-8")
        return img_base64_str

    def isOtpValid(self, otp:int, otp_hash:str):
        totp = pyotp.TOTP(otp_hash)
        l.debug(f"OTP now: {totp.now()}, OTP from user: {otp} ")
        is_otp_valid:bool = totp.verify(otp)
        l.debug(f"is otp valid: {is_otp_valid}")
        return is_otp_valid

    @view_config(route_name='2fa:enable',request_method='POST',  renderer=Conf.enable2fatpl)
    def enable_2fa_post(self):
        otp = self.request.POST.get('otp',None)
        otp_hash = self.request.POST.get('otp_hash',None)
        self.retdict['otp_hash'] = otp_hash
        self.retdict['img_str'] = self.qrcode_img_from_otp_hash(otp_hash=otp_hash)

        if otp and otp_hash:
            otp = int(otp)
            is_otp_valid = self.isOtpValid(otp=otp, otp_hash=otp_hash)

            if is_otp_valid:
                self.user.otp_hash = otp_hash
                msg = {"msg": __(self.request,'Successfully setup 2fa'), "type": "success"}
                self.request.session.flash(msg)
                return HTTPFound(location=self.request.route_url('ppss:user:editself'))
            else:
                self.retdict['errmsg'] = __(self.request,'Otp incorrect or expired ... please retry')
                return self.retdict
        else:
            self.retdict['errmsg'] = __(self.request,'Something went wrong... please retry')
            return self.retdict

    def editUser(self):
        l.info("edit user")
        userid = self.userid
        user = self.user
        selfediting = False
        if self.request.matched_route.name == 'ppss:user:editself':
            userid = self.request.session[Conf.sessionuser]['id']
            user = self.getUserById(userid)
            submiturl = self.request.route_url('ppss:user:editself')
            selfediting = True
        else:
            if userid == self.request.loggeduser.id:
                selfediting = True
                submiturl = self.request.route_url('ppss:user:editself')
            else:
                submiturl = self.request.route_url('ppss:user:edit',elementid=userid)

        l.debug("***{id} -> {user}".format(user=user,id=userid))
        retdict = dict(self.retdict,
            **{
                'msg':"",
                'res':True,
                'userid':userid,
                'submiturl':submiturl,
                'selfediting':selfediting,
                'email_is_required': Conf.email_is_required
        })

        if not user:
            retdict['res'] = False
            retdict['msg'] = __("User not found")

        editablegroups = []

        logged_user = self.request.loggeduser

        l.info("logged user is superuser? {}".format(logged_user.isSuperUser()))
        if logged_user.isSuperUser():
            editablegroups = PPSsgroup.all(self.request.dbsession)
        elif logged_user.hasPermission('edituser') or selfediting:
            editablegroups = logged_user.groups
        l.debug("editablegroups = {}".format(editablegroups))


        requireoldpassowrd = userid >= 0 and ( selfediting or logged_user.isSuperUser()==False )

        retdict.update({"user" : user, 'allgroups':editablegroups,'requireoldpassowrd':requireoldpassowrd })

        if self.request.POST:
            canenable = True

            email = self.request.params.get("email",None)
            if Conf.email_is_required:
                if not email:
                    retdict['msg'] = __( self.request,"Email is required")
                    return retdict
                if not email_is_valid(email):
                    retdict['msg'] = __( self.request,"Email is invalid")
                    return retdict
            if (email != "") and (email != user.email):
                if len(PPSsuser.byField("email",email,self.request.dbsession))>0:
                        retdict['msg'] = "Email '{}' already used.".format(email)
                        return retdict
                
            if userid<0:
                l.debug("this is a post for creation")                
                username = self.request.params.get("username",None)
                if not username:
                    retdict['msg'] = __("Username can not be empty.")
                    return retdict
                if len(PPSsuser.byField("username",username,self.request.dbsession))>0:
                    retdict['msg'] = "Username '{}' already used.".format(username)
                    return retdict
                self.request.dbsession.add(user)
                user.username = username
                #default for new user is "Cant enable". Can be enabled ony if a valid password is supplied
                canenable = False
            username = user.username
            


            if not user:
                return retdict
            
            newpassword = self.request.params.get("password","")
            ##change user password
            if newpassword:
                confirmnewpassword = self.request.params.get("confirmnewpassword","")
                currentpassword = self.request.params.get("currentpassword","")
                l.debug("new password match? {}".format(newpassword==confirmnewpassword) )
                #existing user must match older password (unless edited by superadmin)
                #if (self.request.loggeduser.isSuperUser() == False) or selfediting:
                if requireoldpassowrd:
                    if userid>=0 and (not PPSsuser.checkLogin(username,currentpassword,self.request.dbsession)): 
                        if selfediting:
                            retdict['msg'] = __(self.request,"Your current password does not match!")
                        else:
                            retdict['msg'] = __(self.request,"Current password does not match!")
                        return retdict
                        
                if newpassword==confirmnewpassword:
                    l.info("*****changing password for {}".format(user.username) )
                    res = checkPassword(user,newpassword)
                    l.info("checkPassword result for user {} = {}({})".format(user.username, bool(res),res.getMsg(self.request) ))
                    if res:
                        user.setPassword(newpassword)
                        retdict['msg'] = __(self.request,"Password updated.")
                        canenable = True
                    else:
                        retdict['msg'] = res.getMsg(self.request)
                        #__(self.request,"New password doesn't match constraints." )
                else:
                    retdict['msg'] = __(self.request,"New password doesn't match confirmation field.")
            user.enabled = 1 if self.request.params.get("enabled")=="1" and canenable and user.password else 0
            
            groups=map(int,self.request.params.getall("allgroups"))
            l.debug("group={groups}".format(groups=groups ))
            usergroups = [PPSsgroup.byId(groupid,self.request.dbsession) for groupid in groups if groupid in set([g.id for g in editablegroups ])]
            user.groups = usergroups
            self.request.dbsession.flush()
            #return HTTPFound(self.request.route_url('ppss:user:edit',elementid = user.id) )
            #return retdict
        return retdict

    def listGroup(self):
        elements = self.request.dbsession.query(PPSsgroup).all()
        return dict(self.retdict,**{'elements':elements}) 

    def editGroup(self):
        groupid = int(self.request.matchdict.get("elementid","-1"))
        retdict = dict(self.retdict,**{'msg':"",'res':True,'groupid':groupid} )
        if groupid<0:
            group = PPSsgroup()
        else:
            group = PPSsgroup.byId(groupid,self.request.dbsession)
            if not group:
                return HTTPFound(self.request.route_url('ppss:group:list'))
        retdict.update({'group':group})

        if self.request.POST:  #editing group
            if groupid<0:
                self.request.dbsession.add(group)
            group.name = self.request.params.get("name")
            group.enabled = 1 if self.request.params.get("enablecheck")=="1" else 0
            l.debug("paratri: {p}".format(p=self.request.params ) )
            l.debug("group.name={name},  group.enabled={enabled}".format(name=group.name,enabled=group.enabled))
            elements = self.request.dbsession.query(PPSsgroup).all()
            return dict(retdict,**{'elements':elements})

        elif group:
            allperm = self.request.dbsession.query(PPSspermission).all()
            users = self.request.dbsession.query(PPSsuser).all()
            return render_to_response(  Conf.editgrouptemplate,
                dict(retdict,**{'group':group,'allperm':allperm, 'users': users, 'msg':""}),
                self.request )
        #return HTTPFound(self.request.route_url("ppss:group:list") )

    def listPerm(self):
        elements = self.request.dbsession.query(PPSspermission).all()
        return dict(self.retdict,**{'elements':elements})

    def editPerm(self):
        pid = int(self.request.matchdict.get('elementid',-1) )
        if pid<0:
            perm = PPSspermission(id=pid)
        else:
            perm = PPSspermission.byId(pid,self.request.dbsession)

        if self.request.POST:
            elements = self.request.dbsession.query(PPSspermission).all()
            name = self.request.params.get("name","")
            if pid<0:
                self.request.dbsession.add(PPSspermission(name=name))
            elif perm.permtype!=1:
                perm.name = name
            else:
                res = {'res':False,'msg':__("Can't modify this permission")}
                return dict(self.retdict,dict(res,**{'elements':elements}) )
            res = {'res':True,'msg':__("Permission modified")}
            return dict(self.retdict,**dict(res,**{'elements':elements}) )
        elif perm:
            return render_to_response(  Conf.editpermtemplate,dict(self.retdict,**{'perm':perm}),self.request )
        return HTTPFound(self.request.route_url("ppss:perm:list") )

    def deletePerm(self):
        perm = PPSspermission.byId(int(self.request.matchdict.get('elementid',-1)))

        if perm and perm.permtype != 1:
            self.request.dbsession.delete(perm)
            res = {'res':True,'msg':__("Permission deleted.")}
        else:
            res = {'res':False,'msg':__("Can't delete this permission")}
        elements = self.request.dbsession.query(PPSspermission).all()
        return dict(self.retdict,**dict(res,**{'elements':elements}) ) 



    def addPerm2Group(self):
        perm = PPSspermission.byId(int(self.request.matchdict.get('targetid',-1)),self.request.dbsession)
        group = PPSsgroup.byId(int(self.request.matchdict.get('elementid',-1)),self.request.dbsession)
        if not perm or not group:
            return {'res':False,"msg":__(self.request,"error in ids")}
        for i in group.permissions:
            if i.id == perm.id:
                return {'res':False,"msg":__(self.request,"already present")}
        group.permissions.append(perm)
        l.info(u"adding {perm} to {group}".format(perm=perm,group=group))
        return {'res':True,"msg":"change_perm", "groupperm":group.permdict()}

    def removePerm2Group(self):
        perm = PPSspermission.byId(int(self.request.matchdict.get('targetid',-1)),self.request.dbsession)
        group = PPSsgroup.byId(int(self.request.matchdict.get('elementid',-1)),self.request.dbsession)
        
        if perm and (perm.permtype != 'y'):  #TODO add superadmin capability to do this
            for i,p in enumerate(group.permissions):
                l.info("check {} {}".format(p.id,perm.id) )
                if p.id == perm.id:
                    l.info("match")
                    group.permissions.pop(i)
                    return {'res':True,"msg":"change_perm", "groupperm":group.permdict()}
                else:
                    l.info("no match")


        return {'res':False,'msg':__("Can't remove this permission")}


    def addUser2Group(self):
        user  = PPSsuser.byId(int(self.request.matchdict.get('targetid',-1)),self.request.dbsession)
        group = PPSsgroup.byId(int(self.request.matchdict.get('elementid',-1)),self.request.dbsession)
        if not user or not group:
            return {'res':False,"msg":"error in ids"}
        for i in group.users:
            if i.id == user.id:
                return {'res':False,"msg":__("already present")}
        group.users.append(user)
        l.info(u"adding {user} to {group}".format(user=user,group=group))
        return {'res':True,"msg":"change_user", "elements":group.userdict()}


    def removUser2Group(self):
        user  = PPSsuser.byId(int(self.request.matchdict.get('targetid',-1)),self.request.dbsession)
        group = PPSsgroup.byId(int(self.request.matchdict.get('elementid',-1)),self.request.dbsession)
        if user:  #TODO add superadmin capability to do this
            for i,p in enumerate(group.users):
                if p.id == user.id:
                    group.users.pop(i)
                    return {'res':True,"msg":__(self.request,"change_user"), "elements":group.userdict()}
        return {'res':False,'msg':__(self.request,"Can't remove this permission")}

    def parseqstring(self,qparam):
        if qparam == "" or qparam is None:
            return ""
        qparam = " " + qparam + " "
        qparam = re.sub("[%]+", "\\%", qparam)
        qparam = re.sub("[ ]+", "%", qparam)
        return qparam




    @view_config(route_name='ppss:user:search',permission='listuser',renderer="json")
    def searchUser(self):
        qparam = self.parseqstring(self.request.params.get('q',''))
        l.debug("qparam = {qp}".format(qp=qparam))
        users = self.request.dbsession.query(PPSsuser).filter(PPSsuser.enabled==1).filter(PPSsuser.username.like(qparam)).all()
        return {'res':True,'elements':[u.todict() for u in  users]}

    @view_config(route_name='ppss:group:search',permission='listuser',renderer="json")
    def searchGroup(self):
        qparam = self.parseqstring(self.request.params.get('q',''))
        users = self.request.dbsession.query(PPSsgroup).filter(PPSsgroup.enabled==1).filter(PPSsgroup.name.like(qparam)).all()
        return {'res':True,'elements':[u.todict() for u in  users]}

    @view_config(route_name='ppss:perm:search',permission='listuser',renderer="json")
    def searchParam(self):
        qparam = self.parseqstring(self.request.params.get('q',''))
        users = self.request.dbsession.query(PPSspermission).filter(PPSspermission.name.like(qparam)).all()
        return {'res':True,'elements':[u.todict() for u in  users]}

    @view_config(route_name='test:test',permission='listuser',renderer=Conf.logintemplate)
    def testroute(self):
        return {}

    @view_config(route_name='ppss:user:email:confirm', renderer=Conf.confirm_email_template)
    def confirm_email(self):
        token = self.request.params.get('token', None)
        self.retdict['login_url'] = ""
        if not token:
            self.retdict['msg'] = __(self.request,"Invalid token")
            return self.retdict
        
        hashed_token = getPasswordDigest(token)
        db_token = PPSsResetTokens.firstByField('token', hashed_token, self.request.dbsession)

        if not db_token:
            self.retdict['msg']=__(self.request,"Invalid token")
            return self.retdict
        
        user:PPSsuser = db_token.user
        # lock all tokens of the user
        user_tokens = self.request.dbsession.query(PPSsResetTokens).filter(PPSsResetTokens.user_id == user.id).filter(PPSsResetTokens.reset_type == 'email').with_for_update().all()
            
        matched_token:PPSsResetTokens = None
        for user_token in user_tokens:
            if user_token.token == hashed_token:
                matched_token = user_token
        if not matched_token:
            self.retdict['msg']=__(self.request,"Invalid token")
            return self.retdict
        
        if matched_token.token_expiry < datetime.datetime.now():
            self.retdict['msg']=__(self.request,"Token has expired. Please try again")
            return self.retdict
        
        user.email = matched_token.additionaldata
        if user.enabled == -1:
            user.enabled = 1
        self.retdict['msg'] = __(self.request,"Email confirmed")
        self.retdict['login_url'] = self.request.route_url('ppsslogin')
        for user_token in user_tokens:
            self.request.dbsession.delete(user_token)
        return self.retdict


    @view_config(route_name='ppss:user:recoverpassword', renderer=Conf.recoverpasstemplate)
    def recover(self):
        if self.request.POST:
            email = self.request.params.get("email",None)
            if not email:
                self.retdict['msg'] = __( self.request,"Email is required")
                return self.retdict
            if not email_is_valid(email):
                self.retdict['msg'] = __( self.request,"Email is invalid")
                return self.retdict
            user:PPSsuser = PPSsuser.firstByField('email', email, self.request.dbsession)
            l.info("user is %s", user)
            # same response so that we don’t give attackers any indication that they should try a different email address.
            self.retdict['msg'] = __(self.request, "Please check your email for reset link")
            if user:
                token = secrets.token_urlsafe()
                hashed_token = getPasswordDigest(token)
                user_token = PPSsResetTokens(token=hashed_token, reset_type='password')
                user.tokens.append(user_token)
                sendPasswordResetEmailUseCase(self.request).run(user=user, token=token)
        return self.retdict

    @view_config(route_name='ppss:user:resetpassword', renderer=Conf.resetpasstpl)
    def reset_password(self):
        
        token = self.request.params.get('token', None)
        self.retdict['token'] = token
        self.retdict['login_url'] = ""
            
        if self.request.POST:
            token = self.request.params.get('reset-token', None)
            if not token:
                self.retdict['msg']=__(self.request,"Invalid token")
                return self.retdict
            hashed_token = getPasswordDigest(token)
            db_token = PPSsResetTokens.firstByField('token', hashed_token, self.request.dbsession)
            if not db_token:
                self.retdict['msg']=__(self.request,"Invalid token")
                return self.retdict
            user:PPSsuser = db_token.user

            # lock all tokens of the user
            user_tokens = self.request.dbsession.query(PPSsResetTokens).filter(PPSsResetTokens.user_id == user.id).filter(PPSsResetTokens.reset_type == 'password').with_for_update().all()
            
            matched_token:PPSsResetTokens = None
            for user_token in user_tokens:
                if user_token.token == hashed_token:
                    matched_token = user_token
            if not matched_token:
                self.retdict['msg']=__(self.request,"Invalid token")
                return self.retdict
            
            if matched_token.token_expiry < datetime.datetime.now():
                self.retdict['msg']=__(self.request,"Token has expired. Please try again")
                return self.retdict
            
            # validate input
            newpassword = self.request.params.get("newpassword")
            confirmnewpassword = self.request.params.get("confirmnewpassword","")
            if newpassword!=confirmnewpassword:
                self.retdict['msg']=__(self.request,"Password check doesn't match the password.")
                return self.retdict
            # validate magic number
            
            res = checkPassword(user,newpassword)
            if res:
                user.setPassword(newpassword)
                self.retdict['msg'] = __(self.request,"Password updated.")
                self.retdict['login_url'] = self.request.route_url('ppsslogin')
                for user_token in user_tokens:
                    self.request.dbsession.delete(user_token)
            else:
                self.retdict['msg'] = res.getMsg(self.request)
            
            return self.retdict
            
            
        return self.retdict


import re
EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")
def email_is_valid(email):
    if EMAIL_REGEX.match(email):
        return True
    return False
