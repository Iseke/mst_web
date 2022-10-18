from celery import shared_task
from apps.users import utils


@shared_task
def send_confirmation_email_task(domain, uid, token, email, template):
    utils.send_confirmation_link(domain, uid, token, email, template)
