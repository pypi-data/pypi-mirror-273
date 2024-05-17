<%inherit file="${context['midtpl']}" />

<div class="row">
    <div class="${bc['xs']}12 col-sm-6">
        <form action="${request.route_url('ppss:perm:edit',elementid=perm.id)}" method="POST">
            <input type="hidden" value="${get_csrf_token()}" name="csrf_token">    
            <input class="form-control" type="text" name="name" placeholder="${_('permissionname', domain='ppss_auth')}" value="${perm.name}">
            <br/>
            <input class="btn btn-success" type="submit" name="submit" value="${_('Apply', domain='ppss_auth')}"/>
        </form>
    </div>
</div>