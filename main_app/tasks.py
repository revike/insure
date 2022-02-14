import time

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task()
def send_email_company(**kwargs):
    subject = f'Отклик на заявку "{kwargs["product_name"].capitalize()}"'
    message = f'На заявку откликнулся ' \
              f'{kwargs["first_name"].title()} ' \
              f'{kwargs["last_name"].title()}\n' \
              f'E-mail: {kwargs["email"]}\n' \
              f'Tel: {kwargs["phone"]}\n\n' \
              f'Продукт: \n{kwargs["product_name"]}'
    time.sleep(2)
    return send_mail(subject, message, settings.EMAIL_HOST_USER,
                     [kwargs["company_email"], ],
                     fail_silently=False)
