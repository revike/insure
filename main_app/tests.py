from django.core.management import call_command
from django.test import TestCase, Client

from auth_app.models import CompanyUserProfile, CompanyUser
from insure.settings import DATABASES
from main_app.models import ProductCategory, ProductOption, Product


class TestMainApp(TestCase):
    databases = DATABASES

    def setUp(self):
        call_command('flush', '--noinput')
        test_category = ProductCategory.objects.create(
            name='test', is_active=True)
        test_company = CompanyUser.objects.create_user(
            username='test', email='test@mail.local', password='pass',
            last_name='test', first_name='test', is_active=True)
        test_company_profile = CompanyUserProfile.objects.create(
            company=test_company, name='test_company', tax_id=123,
            is_active=True)
        test_product = Product.objects.create(
            category=test_category, company=test_company_profile,
            name='test_product', short_desc='test_short_desc', is_active=True)
        ProductOption.objects.create(product=test_product, term=0,
                                     is_active=True)
        self.client = Client()

    def test_main_app_urls(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/product/')
        self.assertEqual(response.status_code, 200)

    def test_category_pages(self):
        for category in ProductCategory.objects.all():
            response = self.client.get(f'/category/{category.pk}/')
            self.assertEqual(response.status_code, 200)

    def test_product_pages(self):
        for product in ProductOption.objects.all():
            response = self.client.get(f'/product/{product.pk}/')
            self.assertEqual(response.status_code, 200)
