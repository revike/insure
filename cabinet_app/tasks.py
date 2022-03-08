import time

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse

from auth_app.models import CompanyUser


@shared_task()
def send_email_confirm(user_id, user_name):
    admins = CompanyUser.objects.filter(is_staff=True)
    email_admins = []
    for email_admin in admins:
        email_admins.append(email_admin.email)
    link = reverse('admin:auth_app_companyuser_change', args=[user_id])
    subject = 'Проверка учетной записи'
    message = f' Пользователь {user_name} просит подтвердить его учетную запись\n{settings.DOMAIN_NAME}{link}'
    time.sleep(2)
    return send_mail(subject, message, settings.EMAIL_HOST_USER,
                     email_admins, fail_silently=False)
