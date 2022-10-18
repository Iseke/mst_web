from django.conf import settings
from django.core.mail import send_mail

from celery import shared_task


@shared_task
def send_notification(receiver, data):
    title = f'''{data['name']} task has been changed!'''
    message = f'''Status of {data['name']} task with id {data['id']} has been changed to {data['is_done']}'''
    mail_sent = send_mail(title, message, settings.EMAIL_FROM, [receiver])
    return mail_sent
