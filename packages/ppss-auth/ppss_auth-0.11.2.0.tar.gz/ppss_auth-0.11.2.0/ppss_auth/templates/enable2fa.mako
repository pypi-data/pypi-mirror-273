<%inherit file="${context['midtpl']}" />

<div class="row">
    <div class="${bc['xs']}12 col-sm-6 offset-sm-3">
        <a class="btn btn-secondary my-2" href="${request.route_url('ppss:user:editself')}">Back</a>
        <div class="text-center">
            %if errmsg:
            <div class="alert alert-danger">
                ${errmsg}
            </div>
            %endif
            <p>Add this account to your authenticator app, scanning this QR code </p>
            <img class="mb-3 width=" 200" height="200" src="${img_str}" alt="">
            <p>After setting up you account confirm inserting in the form below 6 digit provided by your auth app</p>
            <form method="post">
                <input type="hidden" value="${get_csrf_token()}" name="csrf_token">
                <input type="hidden" name="otp_hash" value="${otp_hash}">
                <input class="form-control mb-3" placeholder="OTP" inputMode="numeric" type="number" name="otp">
                <button class="btn btn-success" type="submit">Confirm</button>
            </form>
        </div>
    </div>
</div>