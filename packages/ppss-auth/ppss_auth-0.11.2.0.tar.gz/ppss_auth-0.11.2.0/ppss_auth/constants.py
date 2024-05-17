from pyramid.settings import asbool, aslist
import sys
#import types
PY2 = sys.version_info[0] == 2

import os,datetime,logging
l = logging.getLogger('ppssauth')

if PY2:
    def is_nonstr_iter(v):
        return hasattr(v, '__iter__')
else:
    def is_nonstr_iter(v):
        if isinstance(v, str):
            return False
        return hasattr(v, '__iter__')

def getBT(version = 4):
    v4 = version == 4
    return {
        'xs': 'col-' if v4 else 'col-xs-'
    }

class Conf():

    @classmethod
    def tplpath(cls, filename, layout=False):
        path = ""
        if cls.templatepackage:
            path += cls.templatepackage + ":"
        if layout:
            path += cls.templatelayoutfolder
        else:
            path += cls.templatefolder
        return path + "/" + filename + "." + cls.templateextension

    @staticmethod
    def conf2list(confval,default=None):
        try:
            if not is_nonstr_iter(confval):
                confval = aslist(confval,flatten=False)
            return confval
        except Exception as e:
            l.exception(u"Exception parsing value:{}".format(confval))
            if default is None:
                raise e
            else:
                return default

    @classmethod
    def setup(cls, settings):
        cls.adminname   =settings.get("ppss_auth.adminname", "admin")
        cls.adminpass   =settings.get("ppss_auth.adminpass", "")
        cls.initdb = settings.get("ppss_auth.initdb", "true").lower() == 'true'

        # routes
        cls.loginurl = settings.get("ppss_auth.login_url", "/login")
        cls.logouturl = settings.get("ppss_auth.logout_url", "/logout")
        cls.postlogoutroute = settings.get("ppss_auth.post_logout_route", "ppsslogin")
        cls.postloginroute = settings.get("ppss_auth.post_login_route", "home")
        cls.postloginfollow = settings.get("ppss_auth.post_login_follow", "true").lower() == 'true'

        cls.backfromppssauth = settings.get("ppss_auth.back_from_ppss_auth",None)
        
        # NEW USER REGISTRATION
        cls.registeruurl = settings.get("ppss_auth.register_url", "/register")
        cls.usercanregister = settings.get("ppss_auth.canregister", "false").lower() == "true"
        cls.activationemail = settings.get("ppss_auth.register_requireactivation", "true").lower() != "false"

        cls.newusergroups = [x for x in map(str.strip, ( settings.get("ppss_auth.newusergroups", '' ).split(",") ) ) if x  ] if settings.get("ppss_auth.newusergroups", '' ) else ['signeduser']
        cls.saltforhash = settings.get("ppss_auth.salt", "ImTheSaltOfThisLife")

        cls.forbiddentologin = settings.get("ppss_auth.forbidden_to_login", "true").lower() == 'true'

        
        

        #password enforcement
        cls.passwordpreviousdifferent = int(settings.get("ppss_auth.password_previuos_diff",3))
        cls.passwordminlen = int(settings.get("ppss_auth.password_min_len",12))
        cls.passwordrelist = Conf.conf2list( settings.get("ppss_auth.password_relist",["[A-Z]+","[a-z]+","[0-9]+","[!,\.\?\\/;:_\-+*@\£\$\%\&\(\)\"\'=\^àèìòùé\#§°ç{}]+",".{{{len},}}".format(len=cls.passwordminlen)]) )
        cls.forbiddenpasswordlist = settings.get("ppss_auth.forbidden_password_list","")
        #cls.passwordwrongmessage = f'La nuova password deve essere differente dalle precedenti {cls.passwordpreviousdifferent} e avere almeno 12 caratteri, una maiuscola, una minuscola, un numero e un carattere fra "!,.?\\/;:_-+*".'
        cls.passwordwrongmessage = f'The new password must be different from the previous {cls.passwordpreviousdifferent} and should contain at least {cls.passwordminlen} chars, cotaining at least 1 upper case, 1 lower case, 1 number and a special char among these "!,.?\\/;:_-+*".'
        cls.passwordexpiredmessage = 'Password expired. Please change it.'
        cls.passwordexpire =  int(settings.get("ppss_auth.password_expire",0)  )

        cls.loginfailthreshold = int(settings.get("ppss_auth.login_fail_threshold",5)  )
        cls.loginfailinterval = int(settings.get("ppss_auth.login_fail_interval",60)  )

        ##template path
        cls.templatepackage =       settings.get("ppss_auth.templatepackage", "ppss_auth")
        cls.templatefolder =        settings.get("ppss_auth.templatefolder", "/templates")
        cls.templatelayoutfolder =  settings.get("ppss_auth.templatelayoutfolder", "/templates/layouts")
        cls.templateextension =     settings.get("ppss_auth.templateextension", "mako")

        #public templates
        cls.logintemplate = settings.get("ppss_auth.logintemplate", cls.tplpath("login") )
        cls.changepasswordtemplate = settings.get("ppss_auth.changepasswordtemplate", cls.tplpath("change") )
        cls.publictemplateinherit = settings.get("ppss_auth.publictemplateinherit", cls.tplpath("public", True) )
        cls.confirm_email_template = settings.get("ppss_auth.confirm_email_template", cls.tplpath("confirm_email") )

        #bo template
        cls.listusertemplate = settings.get("ppss_auth.listuser_template", cls.tplpath("listuser") )
        cls.editusertemplate = settings.get("ppss_auth.edituser_template", cls.tplpath("edituser") )
        cls.listgrouptemplate = settings.get("ppss_auth.listgroup_template", cls.tplpath("listgroup") )
        cls.editgrouptemplate = settings.get("ppss_auth.editgroup_template", cls.tplpath("editgroup") )
        cls.listpermtemplate = settings.get("ppss_auth.listperm_template", cls.tplpath("listperm") )
        cls.editpermtemplate = settings.get("ppss_auth.editperm_template", cls.tplpath("editperm") )
        cls.registerusertemplate = settings.get("ppss_auth.registeruser_template", cls.tplpath("registeruser") )

        cls.botemplateinherit = settings.get("ppss_auth.botemplateinherit", cls.tplpath("public", True) )
        

        #bo template inheritance
        cls.mastertemplateinherit = settings.get("ppss_auth.mastertemplateinherit", cls.tplpath("masterlayout", True) )
        cls.sectiontemplateinherit = settings.get("ppss_auth.sectiontemplateinherit", cls.tplpath("midlayout", True) )

        cls.bootstrapClasses = getBT(int(settings.get("ppss_auth.bootstrapversion",4)))

        cls.testurl = settings.get("ppss_auth.testurl", "/test")

        


        #Setup user, groups and permissions
        cls.perm2create = Conf.conf2list( settings.get("ppss_auth.permission_list",[])  )
        cls.group2create = Conf.conf2list( settings.get("ppss_auth.group_list",[])  )
        cls.user2create = Conf.conf2list( settings.get("ppss_auth.user_list",[])  )
        cls.defaultpassword = settings.get("ppss_auth.default_password",None)  
        


        #session names
        cls.sessionuser = 'ppss_auth_loggeduser'
        cls.sessionprincipals = 'ppss_auth_principals'
        cls.sessionpermissions = 'ppss_auth_permissions'


        cls.idclient = "896890850990-kdppue1lijfhkj5s7tu8lsh7gsj99ndj.apps.googleusercontent.com"
        cls.secret = "hhuJLuYo9ZnvAVd9XopH-s8n"


        #SMTP
        cls.smtpuser = settings.get("ppss_auth.smtpuser",None)
        cls.smtppassword = settings.get("ppss_auth.smtppassword",None)
        cls.smtphost = settings.get("ppss_auth.smtphost",None)
        cls.smtpport = settings.get("ppss_auth.smtpport",None)
        cls.sender_name = settings.get("ppss_auth.sender_name",None)
        cls.sender_email = settings.get("ppss_auth.sender_email",None)

        #email
        cls.email_is_required = settings.get("ppss_auth.email_is_required", "true").lower() == 'true'
        cls.activationemailtpl = settings.get("ppss_auth.register_activationemailtpl",cls.tplpath('email/activation'))

        cls.recoverpasstemplate = settings.get("ppss_auth.recoverpasstemplate", cls.tplpath('recover'))
        cls.resetpassmailtpl = settings.get("ppss_auth.resetpassmailtpl", cls.tplpath('email/recover'))
        cls.resetpasstpl = settings.get("ppss_auth.resetpasstpl", cls.tplpath('reset'))
        # 2fa
        cls.issuer2fa = settings.get("ppss_auth.issuer2fa", None)
        cls.enable2fatpl = settings.get("ppss_auth.enable2fatpl", cls.tplpath('enable2fa'))
        cls.verify2fatpl = settings.get("ppss_auth.verify2fatpl", cls.tplpath('verify2fa'))
        # turnstile captcha
        cls.turnstile_sitekey = settings.get("ppss_auth.turnstile_sitekey", None)
        cls.turnstile_secretkey = settings.get("ppss_auth.turnstile_secretkey", None)