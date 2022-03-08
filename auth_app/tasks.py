import time

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse


@shared_task()
def send_verify_email(**kwargs):
    verify_link = reverse('auth_app:verify', args=[
        kwargs['email'], kwargs['activation_key']])
    subject = 'Подтверждение учетной записи'
    message = f'Для подтверждения учетной записи' \
              f' {kwargs["username"]} на сайте \
    {settings.DOMAIN_NAME} перейдите по ссылке: ' \
              f'\n{settings.DOMAIN_NAME}{verify_link}'
    time.sleep(2)
    return send_mail(subject, message, settings.EMAIL_HOST_USER,
                     [kwargs['email']], fail_silently=False)


@shared_task()
def send_email_user(email):
    subject = 'Подтверждение учетной записи'
    message = f'Ваша учетная запись успешно прошла подтверждение' \
              f' или изменена на сайте {settings.DOMAIN_NAME}'
    time.sleep(2)
    return send_mail(subject, message, settings.EMAIL_HOST_USER, [email],
                     fail_silently=False)
