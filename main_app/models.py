from django.core.validators import RegexValidator
from django.db import models
from auth_app.models import CompanyUserProfile, CompanyUser
from djongo import models as mongo_models


class ProductCategory(models.Model):
    """Модель категории продукта"""

    class Meta:
        verbose_name_plural = 'категории продуктов'
        verbose_name = 'категории продуктов'

    name = models.CharField(max_length=64, unique=True,
                            verbose_name='название категории')
    description = models.TextField(blank=True, verbose_name='описание')
    is_active = models.BooleanField(default=True, db_index=True,
                                    verbose_name='активна')

    @classmethod
    def get_categories(cls):
        """Возвращает список категорий"""
        return cls.objects.filter(is_active=True)

    def __str__(self):
        return f'{self.name}'


class Product(models.Model):
    """Модель продукта"""

    class Meta:
        verbose_name_plural = 'продукты'
        verbose_name = 'продукты'

    category = models.ForeignKey(to=ProductCategory, on_delete=models.CASCADE,
                                 db_index=True, verbose_name='категория')
    company = models.ForeignKey(to=CompanyUserProfile,
                                on_delete=models.CASCADE,
                                verbose_name='компания')
    name = models.CharField(max_length=128, verbose_name='название продукта')
    short_desc = models.CharField(max_length=128,
                                  verbose_name='краткое описание')
    description = models.TextField(verbose_name='описание', blank=True)
    is_active = models.BooleanField(default=True, verbose_name='активна',
                                    db_index=True)

    def __str__(self):
        return f'{self.name} Категория: {self.category}'


class ProductOption(models.Model):
    """Модель опций продукта"""

    class Meta:
        verbose_name_plural = 'опции продукта'
        verbose_name = 'опции продукта'
        ordering = ['-id']

    product = models.ForeignKey(to=Product, on_delete=models.CASCADE,
                                db_index=True, verbose_name='продукт')
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0,
                                verbose_name='цена')
    term = models.PositiveIntegerField(verbose_name='срок в месяцах')
    rate = models.DecimalField(max_digits=4, decimal_places=2, default=0,
                               blank=True, verbose_name='процентная ставка')
    is_active = models.BooleanField(default=True, verbose_name='активна',
                                    db_index=True)

    @classmethod
    def get_product_for_category(cls, category):
        """Возвращает продукты для определенной категории"""
        return cls.objects.filter(is_active=True,
                                  product__is_active=True,
                                  product__category__is_active=True,
                                  product__company__is_active=True,
                                  product__company__company__is_active=True,
                                  product__category=category)

    def __str__(self):
        return f'{self.product}, {self.price} на {self.term} мес.'


class ProductResponse(models.Model):
    """Модель отклика на продукт"""

    class Meta:
        verbose_name_plural = 'отклики'
        verbose_name = 'отклики'
        ordering = ['-is_active', '-created']

    product = models.ForeignKey(to=ProductOption, on_delete=models.CASCADE,
                                db_index=True, verbose_name='продукт')
    last_name = models.CharField(max_length=150, blank=False,
                                 verbose_name='фамилия')
    first_name = models.CharField(max_length=150, blank=False,
                                  verbose_name='имя')
    patronymic = models.CharField(max_length=150, blank=True,
                                  verbose_name='отчество')
    email = models.EmailField(blank=False, verbose_name='email')
    phone_regex = RegexValidator(regex=r'^\+7\d{10,10}$',
                                 message="Format: +79876543210")
    phone_number = models.CharField(validators=[phone_regex], max_length=12,
                                    blank=False, verbose_name='телефон')
    is_active = models.BooleanField(default=True, verbose_name='активна',
                                    db_index=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='создан')

    @classmethod
    def get_response_length(cls, user_id):
        return cls.objects.filter(
            is_active=True,
            product__product__company__company__id=user_id).count()

    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.product}'


class PageHit(mongo_models.Model):
    """Модель счетчика просмотра страниц"""
    _id = mongo_models.BigAutoField(primary_key=True)
    url = mongo_models.CharField(unique=True, max_length=256,
                                 verbose_name='url')
    count = mongo_models.PositiveBigIntegerField(
        default=1, verbose_name='количество просмотров')
    updated = mongo_models.DateTimeField(auto_now=True, verbose_name='изменен')

    class Meta:
        db_table = 'mongodb'

    def __str__(self):
        return f'{self.url} => {self.count} => {self.updated}'
