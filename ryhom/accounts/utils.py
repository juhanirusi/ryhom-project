from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from .tokens import account_token_generator


def send_registration_confirm_email(self, user, to_email):
    """
    A function used to send a new user a registration email that
    contains a link that they can use to activate their account.
    """
    current_site = get_current_site(self.request)

    mail_subject = 'Welcome To Ryhom.com! Just One More Step...'
    message = render_to_string(
        'accounts/account-verification-email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_token_generator.make_token(user),
    })

    email = EmailMessage(
        mail_subject,
        message,
        from_email='noreply@ryhom.com',
        to=[to_email],
    )
    email.send()
