<%inherit file="${context['supertpl']}" />
<%block name="ppssauth_css">
   <link rel="stylesheet" href="${ request.static_url('ppss_auth:ppss_auth_static/ppssauth.css') }"/>
</%block>

<%block name="ppssauth_headerjs">
<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.7.1/jquery.min.js" integrity="sha512-v2CJ7UaYy4JwqLDIrZUI/4hqeoQieOmAZNXBeQyjo21dadnwR+8ZaIJVT8EE2iyI61OV8e6M8PP2/4hpQINQ/g==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/handlebars.js/4.7.8/handlebars.min.js" integrity="sha512-E1dSFxg+wsfJ4HKjutk/WaCzK7S2wv1POn1RRPGh8ZK+ag9l244Vqxji3r6wgz9YBf6+vhQEYJZpSjqWFPg9gg==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jqueryui/1.13.2/jquery-ui.min.js" integrity="sha512-57oZ/vW8ANMjR/KQ6Be9v/+/h6bq9/l3f0Oc7vn6qMqyhvPd1cvKBRWWpzu0QoneImqr2SkmO4MSqU+RpHom3Q==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>
</%block>

<%block name="ppssauth_footerjs">
</%block>


<div class="usermenu">
	<ul>
    % if request.ppssauthconf.backfromppssauth:
      <li><a href="${request.route_url(request.ppssauthconf.backfromppssauth)}"> < </a></li>
    % endif
		<li class="${'active' if activemenu=='user' else ''}"><a href="${request.route_url('ppss:user:list')}">${_('Users', domain='ppss_auth')}</a></li>
		<li class="${'active' if activemenu=='group' else ''}"><a href="${request.route_url('ppss:group:list')}">${_('Groups', domain='ppss_auth')}</a></li>
		<li class="${'active' if activemenu=='perm' else ''}"><a href="${request.route_url('ppss:perm:list')}">${_('Permissions', domain='ppss_auth')}</a></li>
	</ul>

</div>
<div>


${next.body()}
</div>

