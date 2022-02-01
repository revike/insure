from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse


def send_verify_email(user):
    verify_link = reverse('auth_app:verify', args=[
        user.email, user.activation_key])
    subject = 'Подтверждение учетной записи'
    message = f'Для подтверждения учетной записи {user.username} на сайте \
    {settings.DOMAIN_NAME} перейдите по ссылке: ' \
              f'\n{settings.DOMAIN_NAME}{verify_link}'
    return send_mail(subject, message, settings.EMAIL_HOST_USER,
                     [user.email], fail_silently=False)
