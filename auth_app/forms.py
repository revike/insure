import hashlib
import random

from captcha.fields import CaptchaField
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError

from auth_app.models import CompanyUser


class CompanyUserRegisterForm(UserCreationForm):
    """Форма регистрации"""
    Captcha = CaptchaField(label='Подтвердите что вы не робот!')

    class Meta:
        model = CompanyUser
        fields = ('username', 'last_name', 'first_name', 'patronymic', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''

    def clean_email(self):
        email_user = self.cleaned_data['email']
        email_data = CompanyUser.objects.filter(email=email_user)
        if email_data:
            raise ValidationError(
                'Пользователь с таким email уже зарегистрирован'
            )
        return email_user

    def save(self, **kwargs):
        user = super().save()
        user.is_active = False
        salt = hashlib.sha1(
            str(random.random()).encode('utf8')).hexdigest()[:6]
        user.activation_key = hashlib.sha1(
            (user.email + salt).encode('utf8')).hexdigest()
        user.save()
        return user


class CompanyUserLoginForm(AuthenticationForm):
    """Форма авторизации"""

    class Meta:
        model = CompanyUser
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
