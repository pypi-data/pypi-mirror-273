<%page args="htmlclass='', tag='div'"/>


<${tag} class="ppss_auth--userblock ${htmlclass}">
  % if 'ppss_auth_loggeduser' in request.session:
    ${_('Hi', domain='ppss_auth')} <strong><a href="${request.route_url('ppss:user:editself')}">${request.session['ppss_auth_loggeduser']['name']}</a></strong><br>
    <small>${_('Not', domain='ppss_auth')} ${request.session['ppss_auth_loggeduser']['name']}? <a href="${request.route_url('ppsslogout')}">Logout</a></small>
  % else:
    <a href="${request.route_url('ppsslogin')}">${_('Login', domain='ppss_auth')}</a>
  % endif
</${tag}>