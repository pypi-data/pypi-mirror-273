import smtplib
import ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Sequence
from ppss_auth.models import PPSsuser

from pyramid.request import Request
from pyramid.renderers import render
from ..constants import Conf
from ..ppss_auth_utils import _, __


import logging

logger = logging.getLogger(__name__)


__emailclient = None


def getClient():
    global __emailclient
    if __emailclient is None:
        __emailclient = Mailer(
            Conf.smtpuser, Conf.smtppassword, Conf.smtphost, Conf.smtpport
        )
    return __emailclient


class MailMessage:
    def __init__(
        self,
        request: Request,
        subject: str,
        from_name: str,
        from_email: str,
        to_addrs: Sequence[str],
        cc_addrs: Sequence[str] = None,
    ) -> None:
        self.request = request
        self.subject = subject
        self.from_name = from_name
        self.from_email = from_email
        self.to_addrs = to_addrs
        self.cc_addrs = cc_addrs if cc_addrs else ()
        self.message = self.setup_message()

    def setup_message(self) -> MIMEMultipart:
        message = MIMEMultipart("mixed")
        message["Subject"] = self.subject
        message["From"] = "{} <{}>".format(self.from_name, self.from_email)
        message["To"] = ",".join(self.to_addrs)
        message["Cc"] = ",".join(self.cc_addrs)
        return message

    def get_message(self):
        return self.message

    def get_from_address(self):
        return self.from_email

    def get_to_addrs(self):
        return self.to_addrs + self.cc_addrs

    def render_template(self, text: str, template: str, template_data: dict):
        # template = "ppss_auth:templates/email/" + template + ".jinja2"
        # template = f"{Conf.templatepackage}:{Conf.templatefolder}/{template}.{Conf.templateextension}"
        context = {**template_data, "text": text}
        logger.info("template_data = %s", context)
        return render(template, context, self.request)

    def add_body(self, text: str, template: str, template_data: dict):
        message_alternative = MIMEMultipart("alternative")
        message_related = MIMEMultipart("related")

        html = self.render_template(text, template, template_data)

        message_related.attach(MIMEText(html, "html"))
        message_alternative.attach(MIMEText(text, "plain"))
        message_alternative.attach(message_related)

        self.message.attach(message_alternative)

    def __repr__(self) -> str:
        return f"<MailMessage subject={self.subject}, to={self.to_addrs}>"


class Mailer:
    def __init__(self, user, password, host, port):
        self.user = user
        self.password = password
        self.host = host
        self.port = port

    def __send(self, server, msg):
        server.sendmail(
            from_addr=msg.get_from_address(),
            to_addrs=msg.get_to_addrs(),
            msg=msg.get_message().as_string(),
        )

    def send(self, msg: MailMessage):
        if self.user:
            context = ssl.create_default_context()
            with smtplib.SMTP(self.host, self.port) as server:
                server.starttls(context=context)
                server.login(self.user, self.password)
                self.__send(server, msg)
        else:
            with smtplib.SMTP(self.host, self.port) as server:
                self.__send(server, msg)
        logger.info("Successfully sent %s", msg)


class sendConfirmEmailUseCase:
    def __init__(self, request: Request) -> None:
        self.request = request

    def run(self, user: PPSsuser,email:str, token: str, tpl=Conf.activationemailtpl):
        mailer = getClient()
        message = MailMessage(
            request=self.request,
            subject=__(self.request, "Confirm email"),
            from_name=Conf.sender_name,
            from_email=Conf.sender_email,
            to_addrs=(email,)
        )
        confirm_link = self.request.route_url(
            "ppss:user:email:confirm", _query={'token':token}
        )
        text = (
            __(self.request, "Confirm your email following this link: ")
            + confirm_link
        )
        message.add_body(
            text=text,
            template=tpl,
            template_data={"user": user, "confirm_link": confirm_link},
        )
        mailer.send(msg=message)

class sendPasswordResetEmailUseCase:
    def __init__(self, request: Request) -> None:
        self.request = request

    def run(self, user: PPSsuser, token: str, tpl=Conf.resetpassmailtpl):
        mailer = getClient()
        message = MailMessage(
            request=self.request,
            subject=__(self.request, "Reset password"),
            from_name=Conf.sender_name,
            from_email=Conf.sender_email,
            to_addrs=(user.email,)
        )
        reset_link = self.request.route_url(
            "ppss:user:resetpassword",  _query={'token':token}
        )
        text = (
            __(self.request, "We received a reset/recover password request from this email address. If it was you, to reset your password follow or enter in your browser's navigation bar this link: ")
            + reset_link
        )
        message.add_body(
            text=text,
            template=tpl,
            template_data={"user": user, "reset_link": reset_link},
        )
        mailer.send(msg=message)  
