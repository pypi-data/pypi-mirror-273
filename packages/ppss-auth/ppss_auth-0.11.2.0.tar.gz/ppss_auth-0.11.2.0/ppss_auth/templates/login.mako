<%inherit file="${context['logintpl']}" />
<div class="container">
    <div class="row text-center">
        <div class="${bc['xs']}12 col-md-4 offset-md-4">
            <form class="my-5" action="${request.route_url('ppsslogin')}" method="POST" class="loginform">
                <input type="hidden" value="${get_csrf_token()}" name="csrf_token">
                <h1 class="h3 mb-3 font-weight-normal">${_("Please sign in", domain='ppss_auth')}</h1>
                % if request.loggeduser: 
                <p>
                    ${_('You are already logged in as', domain='ppss_auth')} <a href="${request.route_url('ppss:user:editself')}">${request.loggeduser.username}</a>. <a href="${request.route_url('ppsslogout')}">Logout</a>?<br/>
                    ${signinreason}<br/>
                    ${_("You can proceed to your main page following this ") }<a href="${request.route_url(request.ppssauthconf.postloginroute)}">${_("link")}</a>.<br/>
                </p>
                % endif
                <input class="form-control" type="text" name="username" placeholder="${_('username', domain='ppss_auth')}" class="form-control">
                <br/>
                <input class="form-control" type="password" name="password" autocomplete="off" placeholder="${_('password', domain='ppss_auth')}" class="form-control">
                <br/>
                % if isCaptchaEnabled:
                <script src="https://challenges.cloudflare.com/turnstile/v0/api.js" async defer></script>
                <div class="cf-turnstile" data-sitekey="${ppsauthconf.turnstile_sitekey}"></div>
                % endif
                % if email_is_required:
                <p>${_('Forgot password ?',domain='ppss_auth')}   
                <a href="${request.route_url('ppss:user:recoverpassword')}">${_('recover',domain='ppss_auth')}</a></p>
                % endif
                <div class="text-center">
                    <input class="btn btn-success" type="submit" name="submit" value="${_('Login', domain='ppss_auth')}"/>
                    % if ppsauthconf.usercanregister:
                    <br>
                    <small>${_('Not registered yet?', domain='ppss_auth')} <a href="${request.route_url('ppss:user:register')}">${_('Register now', domain='ppss_auth')}</a></small>
                    % endif
                </div>
                <br/>
                <p class="text-danger">${msg}</p>
            </form>
        </div>
    </div>
</div>