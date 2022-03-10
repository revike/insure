import time

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task()
def send_email_feedback(**kwargs):
    subject = f'{kwargs["subject"]}'
    message = f'{kwargs["message"]}\n\nСообщение от ' \
              f'пользователя - {kwargs["name"]}\nE-mail: {kwargs["email"]}'

    time.sleep(2)
    return send_mail(subject, message, settings.EMAIL_HOST_USER,
                     [settings.EMAIL_HOST_USER],
                     fail_silently=False)


@shared_task()
def send_email_feedback_user(**kwargs):
    subject = f'{kwargs["subject"]}'
    message = f'{kwargs["name"]}, Спасибо за обращение!\nМы получили ваше ' \
              f'сообщение и в ближайшее время обязательно вам ответим!'

    time.sleep(2)
    return send_mail(subject, message, settings.EMAIL_HOST_USER,
                     [kwargs['email']],
                     fail_silently=False)
