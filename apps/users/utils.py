from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from apps.users.tokens import account_activation_token
from apps.users.tasks import send_confirmation_email_task


def send_confirmation_link(domain, uid, token, email, template):
    subject = 'Account activation'
    message = render_to_string(template, {
        'domain': domain,
        'uid': uid,
        'token': token,
    })

    default_from_email_address = settings.EMAIL_FROM
    send_mail(subject, message, default_from_email_address, [email], html_message=message)


def pre_send_confirmation_email(request, user, template):
    domain, email = get_current_site(request).domain, user.email
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = account_activation_token.make_token(user)

    send_confirmation_email_task.delay(domain, uid, token, email, template)
