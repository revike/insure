from django.core.management import call_command
from django.test import TestCase, Client
from django.urls import reverse, resolve

from insure.settings import DATABASES
from main_app.forms import ProductResponseCreateForm
from main_app.models import ProductCategory, ProductOption
from main_app.views import IndexView, ProductListView


class TestMainApp(TestCase):
    databases = DATABASES

    def setUp(self):
        call_command('flush', '--noinput')
        call_command('loaddata', 'test_db.json')
        self.client = Client()

    def test_index(self):
        url = reverse('main_app:index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_app/index.html')
        self.assertEquals(resolve(url).func.view_class, IndexView)

    def test_products(self):
        url = reverse('main_app:products')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_app/products.html')
        self.assertEquals(resolve(url).func.view_class, ProductListView)

    def test_category_pages(self):
        for category in ProductCategory.objects.all():
            url = reverse('main_app:category', kwargs={'pk': category.id})
            response = self.client.get(url)
            if category.is_active:
                self.assertEqual(response.status_code, 200)
                self.assertTemplateUsed(response, 'main_app/category.html')
            else:
                self.assertEqual(response.status_code, 200)
                self.assertTemplateUsed(response, 'main_app/category.html')

    def test_product_pages(self):
        for product in ProductOption.objects.all():
            url = reverse('main_app:product', kwargs={'pk': product.id})
            response = self.client.get(url)
            if product.is_active and product.product.is_active and \
                    product.product.category.is_active and \
                    product.product.company.is_active and \
                    product.product.company.company.is_active:
                self.assertEqual(response.status_code, 200)
                self.assertTemplateUsed(response, 'main_app/product.html')
                data = {
                    'first_name': 'Ivan',
                    'last_name': 'Ivanon',
                    'patronymic': 'Ivanovich',
                    'email': 'local@ya.local',
                    'phone_number': '+79999999999',
                }
                response = self.client.post(path=url, data=data)
                self.assertEqual(response.status_code, 302)
            else:
                self.assertEqual(response.status_code, 404)
                self.assertTemplateNotUsed(response, 'main_app/product.html')

    def test_response(self):
        for product in ProductOption.objects.all():
            url = reverse('main_app:valid', kwargs={'pk': product.id})
            response = self.client.get(url)
            if product.is_active and product.product.is_active and \
                    product.product.category.is_active and \
                    product.product.company.is_active and \
                    product.product.company.company.is_active:
                self.assertEqual(response.status_code, 200)
                self.assertTemplateUsed(response,
                                        'main_app/response_valid.html')
            else:
                self.assertEqual(response.status_code, 404)
                self.assertTemplateNotUsed(response,
                                           'main_app/response_valid.html')

    def test_form(self):
        data_true = {
            'first_name': 'Ivan',
            'last_name': 'Ivanon',
            'patronymic': 'Ivanovich',
            'email': 'local@ya.local',
            'phone_number': '+79999999999',
        }
        data_false = {
            'first_name': 'Ivan',
            'last_name': 'Ivanon',
            'patronymic': 'Ivanovich',
            'email': 'local@ya.local',
            'phone_number': '89999999999',
        }
        form = ProductResponseCreateForm(data=data_true)
        self.assertTrue(form.is_valid())
        form = ProductResponseCreateForm(data=data_false)
        self.assertFalse(form.is_valid())
