import mimetypes

from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from .tokens import account_activation_token


def send_account_verification_mail(request, user, email):
    subject = "Account verification link has been sent to you."
    message = render_to_string(
        "registration/account_activation.html",
        {
            "user": user,
            "domain": get_current_site(request).domain,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": account_activation_token.make_token(user),
        },
    )
    email = EmailMessage(subject, message, to=[email])
    email.send()


def send_file_attachment_to_email(request, email, file):
    subject = "Document from file server website"
    email = EmailMessage(subject=subject, body="", to=[email])
    mimetype, _ = mimetypes.guess_type(file.name)
    email.attach(filename=file.name, content=file.read(), mimetype=mimetype)
    email.send()
