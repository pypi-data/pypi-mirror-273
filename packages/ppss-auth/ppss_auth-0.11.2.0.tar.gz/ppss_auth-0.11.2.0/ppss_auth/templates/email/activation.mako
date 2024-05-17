<html>
<body>
  
  ${_("Hello", domain='ppss_auth')} ${user.username},<br/>
  <p>
    ${_("Follow this link to confirm your email", domain='ppss_auth')} <a href="${confirm_link}">Link</a>
  </p>
  <p>
    <a href="${confirm_link}">${confirm_link}</a>
  </p>
</body></html>