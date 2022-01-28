from PIL import Image
from django.contrib.auth.models import AbstractUser
from django.db import models


class CompanyUser(AbstractUser):
    """Модель компании"""

    class Meta:
        verbose_name_plural = 'компании'
        verbose_name = 'компании'

    last_name = models.CharField(max_length=150, blank=False,
                                 verbose_name='фамилия директора')
    first_name = models.CharField(max_length=150, blank=False,
                                  verbose_name='имя директора')
    patronymic = models.CharField(max_length=150, blank=True,
                                  verbose_name='отчество директора')
    email = models.EmailField(blank=False, verbose_name='email')

    def __str__(self):
        return f'{self.username}'


class CompanyUserProfile(models.Model):
    """Модель профиля компании"""

    class Meta:
        verbose_name_plural = 'профили компаний'
        verbose_name = 'профиль компании'

    company = models.OneToOneField(to=CompanyUser, on_delete=models.CASCADE,
                                   verbose_name='компания')
    name = models.CharField(max_length=128, verbose_name='название компании')
    tax_id = models.BigIntegerField(unique=True, db_index=True,
                                    verbose_name='ИНН')
    about_company = models.TextField(blank=True, verbose_name='о компании')
    label = models.ImageField(
        upload_to='company_labels', blank=True, verbose_name='лейбл')

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super().save()
        img = Image.open(self.label.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.label.path)

    def __str__(self):
        return f'{self.name}'
