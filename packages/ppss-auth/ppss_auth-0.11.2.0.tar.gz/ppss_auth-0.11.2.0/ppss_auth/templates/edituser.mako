<%inherit file="${context['midtpl']}" />

<%
usergroups = {}
for g in user.groups:
    usergroups[g.id] = g.name
%>
<div class="row">
    <div class="${bc['xs']}12 col-sm-6">
        %if user and user.username:
        <h3>${_("Edit user {username}", domain='ppss_auth').format(username=user.username)}</h3>
        %endif

        %if request.session.peek_flash():
            %for message in request.session.pop_flash():
            <div class="alert alert-${message.type}" role="alert">
                ${ message.msg }
            </div>
            %endfor
        %endif

        <form action="${submiturl}" method="POST" autocomplete="off">
            <input type="hidden" value="${get_csrf_token()}" name="csrf_token">
            <input type="hidden" name="userid" value="${user.id if (user and user.id) else '-1'}">
            <input class="form-control" type="text" name="username" placeholder="${_('username', domain='ppss_auth')}" value="${user.username if (user and user.username) else ''}">
            </br>
            <input class="form-control" type="email" name="email" placeholder="${_('email', domain='ppss_auth')}" value="${user.email if (user and user.email) else ''}" ${ 'required' if email_is_required else '' } >
            </br>
            %if selfediting or ((request.loggeduser.isSuperUser() == False) and user.id and user.id >= 0):
            <input class="form-control" type="password" name="currentpassword" placeholder="${_('current password', domain='ppss_auth')}" value="">
            </br>
            %endif
            <input class="form-control" type="password" name="password" placeholder="${_('password', domain='ppss_auth')}" value="" autocomplete="new-password">
            </br>
            <input class="form-control" type="password" name="confirmnewpassword" placeholder="${_('confirm new password', domain='ppss_auth')}" value="" autocomplete="new-password">
            %if ppsauthconf.issuer2fa and selfediting and not user.otp_hash:
            <a href="${request.route_url('2fa:enable')}" class="btn btn-primary my-2">${_('Enable 2FA', domain='ppss_auth')}</a>
            %endif
            %if user.otp_hash:
            <div class="form-check">
                <input checked class="form-check-input" type="checkbox" id="defaultCheck2" disabled>
                <label class="form-check-label text-success" for="defaultCheck2">
                    2FA enabled
                </label>
              </div>
            
            %endif
            
            <div class="checkbox">
                <label for="enablecheck">
                    <input id="enablecheck" type="checkbox" value="1" ${'checked="checked"' if user and user.enabled else ''} name="enabled"> ${_('Enable:', domain='ppss_auth')}
                </label>
            </div>
            <p class="label">${_('Groups', domain='ppss_auth')}</p>
            %for g in allgroups:
                <label class="checkbox-inline">
                    <input name="allgroups" type="checkbox" value="${g.id}" ${"checked" if g.id in usergroups else ""}> ${g.name}
                </label>
            %endfor
            </br>
            <input class="btn btn-success" type="submit" name="submit" value="${_('Apply', domain='ppss_auth')}"/>

            <p class="resultmsg">${msg}</p>
        </form>
    </div>
</div>