<%inherit file="${context['midtpl']}" />
<div class="row">
    <div class="${bc['xs']}12">
        ${msg}
        % if login_url:
            <a href="${login_url}">Login</a>
        % endif
    </div>
</div>
