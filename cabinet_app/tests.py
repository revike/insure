from django.core.management import call_command
from django.test import TestCase, Client
from django.urls import reverse, resolve

from auth_app.models import CompanyUserProfile, CompanyUser
from cabinet_app.forms import ProductCreateForm, ProductOptionCreateForm, \
    ProfileUpdateForm, ProfileUpdateDataForm, ProductOptionUpdateForm, \
    ProductUpdateForm
from cabinet_app.views import CabinetIndexView, MyProductListView, \
    ProductCreateView, ProductResponseView, ProfileUpdateView, \
    MyProductUpdateView, MyProductDeleteView
from insure.settings import DATABASES
from main_app.models import ProductCategory, ProductOption, Product


class TestCabinetApp(TestCase):
    """Тест личного кабинета"""
    databases = DATABASES

    def setUp(self):
        call_command('flush', '--noinput')
        call_command('loaddata', 'test_db.json')
        self.client = Client()

    def test_index(self):
        """Тест профиля"""
        url = reverse('cabinet_app:profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        self.client.login(username='admin', password='admin')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertFalse(response.context['user'].is_anonymous)
        self.assertTemplateUsed(response, 'cabinet_app/profile.html')
        self.assertEquals(resolve(url).func.view_class, CabinetIndexView)

    def test_my_products(self):
        """Тест личных продуктов"""
        url = reverse('cabinet_app:my_products')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        self.client.login(username='admin', password='admin')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertFalse(response.context['user'].is_anonymous)
        self.assertTemplateUsed(response, 'cabinet_app/my_products.html')
        self.assertEquals(resolve(url).func.view_class, MyProductListView)

    def test_product_create(self):
        """Тест создания продуктов"""
        url = reverse('cabinet_app:product_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        self.client.login(username='admin', password='admin')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertFalse(response.context['user'].is_anonymous)
        self.assertTemplateUsed(response, 'cabinet_app/product_create.html')
        self.assertEquals(resolve(url).func.view_class, ProductCreateView)

        data_product = {
            'name': 'test',
            'short_desc': 'test',
            'description': 'test',
        }

        data_option = {
            'price': 1,
            'rate': 1
        }

        form = ProductCreateForm(data=data_product)
        self.assertFalse(form.is_valid())

        data_product['category'] = ProductCategory.objects.filter(
            is_active=True).first().id
        form = ProductCreateForm(data=data_product)
        self.assertTrue(form.is_valid())

        form = ProductOptionCreateForm(data=data_option)
        self.assertFalse(form.is_valid())

        data_option['term'] = 1
        form = ProductOptionCreateForm(data=data_option)
        self.assertTrue(form.is_valid())

        data = {**data_product, **data_option}
        self.client.logout()
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)
        new_product = ProductOption.objects.filter(
            product__category=data['category'], product__name=data['name'],
            product__short_desc=data['short_desc'], price=data['price'],
            product__description=data['description'], rate=data['rate'],
            term=data['term']
        )
        self.assertFalse(new_product.count(), 1)

        self.client.login()
        self.client.login(username='admin', password='admin')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_anonymous)
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)
        new_product = ProductOption.objects.filter(
            product__category=data['category'], product__name=data['name'],
            product__short_desc=data['short_desc'], price=data['price'],
            product__description=data['description'], rate=data['rate'],
            term=data['term']
        )
        self.assertTrue(new_product.count(), 1)

    def test_response(self):
        """Тест откликов на личные продукты"""
        url = reverse('cabinet_app:response')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        self.client.login(username='admin', password='admin')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertFalse(response.context['user'].is_anonymous)
        self.assertTemplateUsed(response, 'cabinet_app/response.html')
        self.assertEquals(resolve(url).func.view_class, ProductResponseView)

    def test_profile_update(self):
        """Тест редактирования профиля"""
        for user in CompanyUserProfile.objects.all():
            url = reverse('cabinet_app:profile_update', kwargs={'pk': user.id})
            response = self.client.get(url)
            if user.is_active and user.company.is_active and \
                    user.company.username == 'admin':
                self.assertEqual(response.status_code, 302)
                self.client.login(username='admin', password='admin')
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)
                self.assertFalse(response.context['user'].is_anonymous)
                self.assertTemplateUsed(response,
                                        'cabinet_app/profile_update.html')
                self.assertEquals(resolve(url).func.view_class,
                                  ProfileUpdateView)
                about_company = CompanyUserProfile.objects.filter(
                    company__username='admin').first().about_company
                response = self.client.post(url, data={'about_company': '123'})
                self.assertEqual(response.status_code, 302)
                about_company_finish = CompanyUserProfile.objects.filter(
                    company__username='admin').first().about_company
                self.assertNotEquals(about_company, about_company_finish)
                self.client.logout()
            elif user.is_active and user.company.is_active and \
                    user.company.username != 'admin':
                self.assertEqual(response.status_code, 302)
                self.client.login(username='admin', password='admin')
                response = self.client.get(url)
                self.assertEqual(response.status_code, 404)
                response = self.client.post(url, data={'about_company': '123'})
                self.assertEqual(response.status_code, 404)
                self.client.logout()
            else:
                response = self.client.get(url)
                self.assertEqual(response.status_code, 302)

        form = ProfileUpdateForm(
            data={'about_company': '1', 'label': '2'})
        self.assertTrue(form.is_valid())

    def test_profile_update_data(self):
        """Тест редактирования компании"""
        data = {
            'last_name': 'name',
            'first_name': 'name',
            'patronymic': 'name',
        }

        for user in CompanyUser.objects.all():
            url = reverse('cabinet_app:profile_update_data',
                          kwargs={'pk': user.id})
            response = self.client.get(url)
            if user.is_active and user.username == 'admin':
                self.assertEqual(response.status_code, 302)
                self.client.login(username='admin', password='admin')
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)
                self.assertFalse(response.context['user'].is_anonymous)
                self.assertTemplateUsed(response,
                                        'cabinet_app/profile_update_data.html')
                self.assertEquals(resolve(url).func.view_class,
                                  ProfileUpdateView)
                email = CompanyUser.objects.filter(
                    username='admin').first().email
                self.client.post(url, data=data)
                email_finish = CompanyUser.objects.filter(
                    username='admin').first().email
                self.assertEquals(email, email_finish)
                data['email'] = f'test_{email}'
                self.client.post(url, data=data)
                email_finish = CompanyUser.objects.filter(
                    username='admin').first().email
                self.assertNotEquals(email, email_finish)
                self.client.logout()
            elif user.is_active and user.username != 'admin':
                self.assertEqual(response.status_code, 302)
                self.client.login(username='admin', password='admin')
                response = self.client.get(url)
                self.assertEqual(response.status_code, 404)
                response = self.client.post(url, data=data)
                self.assertEqual(response.status_code, 404)
                self.client.logout()
            else:
                response = self.client.get(url)
                self.assertEqual(response.status_code, 302)

        try:
            data.pop('email')
        except KeyError:
            ...
        form = ProfileUpdateDataForm(data=data)
        self.assertFalse(form.is_valid())
        data['email'] = 'test@local.ru'
        form = ProfileUpdateDataForm(data=data)
        self.assertTrue(form.is_valid())

    def test_product_update(self):
        """Тест редактирования опций продукта"""
        for product in ProductOption.objects.all():
            product_data = ProductOption.objects.filter(id=product.id).first()
            data = {
                'price': product_data.price + 1,
                'term': product_data.price + 1,
                'rate': product_data.price + 1,
            }
            url = reverse('cabinet_app:product_update',
                          kwargs={'pk': product.id})
            response = self.client.get(url)
            if product.is_active and product.product.is_active \
                    and product.product.category.is_active \
                    and product.product.company.is_active \
                    and product.product.company.company.is_active \
                    and product.product.company.company.username == 'admin':
                self.assertEqual(response.status_code, 302)
                self.client.login(username='admin', password='admin')
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)
                self.assertFalse(response.context['user'].is_anonymous)
                self.assertTemplateUsed(response,
                                        'cabinet_app/product_update.html')
                self.assertEquals(resolve(url).func.view_class,
                                  MyProductUpdateView)
                price = ProductOption.objects.filter(
                    id=product.id).first().price
                self.client.post(url, data=data)
                price_finish = ProductOption.objects.filter(
                    id=product.id).first().price
                self.assertNotEquals(price, price_finish)
                self.client.logout()
            elif product.is_active and product.product.is_active \
                    and product.product.category.is_active \
                    and product.product.company.is_active \
                    and product.product.company.company.is_active \
                    and product.product.company.company.username != 'admin':
                self.assertEqual(response.status_code, 302)
                self.client.login(username='admin', password='admin')
                response = self.client.get(url)
                self.assertEqual(response.status_code, 404)
                response = self.client.post(url, data=data)
                self.assertEqual(response.status_code, 404)
                self.client.logout()
            elif (product.is_active == False
                  or product.product.is_active == False
                  or product.product.category.is_active == False
                  or product.product.company.is_active == False
                  or product.product.company.company.is_active == False) \
                    and product.product.company.company.username == 'admin':
                self.assertEqual(response.status_code, 302)
                self.client.login(username='admin', password='admin')
                response = self.client.get(url)
                self.assertEqual(response.status_code, 404)
                response = self.client.post(url, data=data)
                self.assertEqual(response.status_code, 404)
                self.client.logout()
            else:
                response = self.client.get(url)
                self.assertEqual(response.status_code, 302)

        data = {
            'price': '-1',
            'term': '-1',
            'rate': '-1',
        }
        form = ProductOptionUpdateForm(data=data)
        self.assertFalse(form.is_valid())
        data['price'] = '1'
        data['term'] = '1'
        data['rate'] = '1'
        form = ProductOptionUpdateForm(data=data)
        self.assertTrue(form.is_valid())

    def test_product_update_title(self):
        """Тест редактирования продукта"""
        for product in Product.objects.all():
            product_data = Product.objects.filter(id=product.id).first()
            data = {
                'category': f'{product_data.category.name}_test',
                'name': f'{product_data.name}_test',
                'short_desc': f'{product_data.short_desc}_test',
                'description': f'{product_data.description}_test',
            }
            url = reverse('cabinet_app:product_update_title',
                          kwargs={'pk': product.id})
            response = self.client.get(url)
            if product.is_active \
                    and product.category.is_active \
                    and product.company.is_active \
                    and product.company.company.is_active \
                    and product.company.company.username == 'admin':
                self.assertEqual(response.status_code, 302)
                self.client.login(username='admin', password='admin')
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)
                self.assertFalse(response.context['user'].is_anonymous)
                self.assertTemplateUsed(
                    response, 'cabinet_app/product_update_title.html')
                self.assertEquals(resolve(url).func.view_class,
                                  MyProductUpdateView)
                product_name = Product.objects.filter(
                    id=product.id).first().name
                self.client.post(url, data=data)
                product_name_finish = Product.objects.filter(
                    id=product.id).first().name
                self.assertEquals(product_name, product_name_finish)
                data['category'] = Product.objects.filter(
                    id=product.id).first().category.id
                self.client.post(url, data=data)
                product_name_finish = Product.objects.filter(
                    id=product.id).first().name
                self.assertNotEquals(product_name, product_name_finish)
                self.client.logout()
            elif product.is_active \
                    and product.category.is_active \
                    and product.company.is_active \
                    and product.company.company.is_active \
                    and product.company.company.username != 'admin':
                self.assertEqual(response.status_code, 302)
                self.client.login(username='admin', password='admin')
                response = self.client.get(url)
                self.assertEqual(response.status_code, 404)
                response = self.client.post(url, data=data)
                self.assertEqual(response.status_code, 404)
                self.client.logout()
            elif (product.is_active == False
                  or product.category.is_active == False
                  or product.company.is_active == False
                  or product.company.company.is_active == False) \
                    and product.company.company.username == 'admin':
                self.assertEqual(response.status_code, 302)
                self.client.login(username='admin', password='admin')
                response = self.client.get(url)
                self.assertEqual(response.status_code, 404)
                response = self.client.post(url, data=data)
                self.assertEqual(response.status_code, 404)
                self.client.logout()
            else:
                response = self.client.get(url)
                self.assertEqual(response.status_code, 302)

        data = {
            'category': 'test',
            'name': 'test',
            'short_desc': 'test',
            'description': 'test',
        }
        form = ProductUpdateForm(data=data)
        self.assertFalse(form.is_valid())
        data['category'] = 1
        form = ProductUpdateForm(data=data)
        self.assertTrue(form.is_valid())

    def test_product_option_delete(self):
        """Тест удаления опций продукта"""
        for product in ProductOption.objects.all():
            url = reverse('cabinet_app:product_option_delete',
                          kwargs={'pk': product.id})
            response = self.client.get(url)
            if product.is_active and product.product.is_active \
                    and product.product.category.is_active \
                    and product.product.company.is_active \
                    and product.product.company.company.is_active \
                    and product.product.company.company.username == 'admin':
                self.assertEqual(response.status_code, 302)
                self.client.login(username='admin', password='admin')
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)
                self.assertFalse(response.context['user'].is_anonymous)
                self.assertTemplateUsed(
                    response, 'cabinet_app/product_option_delete.html')
                self.assertEquals(resolve(url).func.view_class,
                                  MyProductDeleteView)
                active = ProductOption.objects.filter(
                    id=product.id).first().is_active
                self.client.post(url)
                active_finish = ProductOption.objects.filter(
                    id=product.id).first().is_active
                self.assertNotEquals(active, active_finish)
                response = self.client.get(url)
                self.assertEqual(response.status_code, 404)
                self.client.logout()
            elif product.is_active and product.product.is_active \
                    and product.product.category.is_active \
                    and product.product.company.is_active \
                    and product.product.company.company.is_active \
                    and product.product.company.company.username != 'admin':
                self.assertEqual(response.status_code, 302)
                self.client.login(username='admin', password='admin')
                response = self.client.get(url)
                self.assertEqual(response.status_code, 404)
                self.client.logout()
            elif (product.is_active == False
                  or product.product.is_active == False
                  or product.product.category.is_active == False
                  or product.product.company.is_active == False
                  or product.product.company.company.is_active == False) \
                    and product.product.company.company.username == 'admin':
                self.assertEqual(response.status_code, 302)
                self.client.login(username='admin', password='admin')
                response = self.client.get(url)
                self.assertEqual(response.status_code, 404)
                self.client.logout()
            else:
                response = self.client.get(url)
                self.assertEqual(response.status_code, 302)

    def test_product_delete(self):
        """тест удаления продукта"""
        for product in Product.objects.all():
            url = reverse('cabinet_app:product_delete',
                          kwargs={'pk': product.id})
            response = self.client.get(url)
            if product.is_active \
                    and product.category.is_active \
                    and product.company.is_active \
                    and product.company.company.is_active \
                    and product.company.company.username == 'admin':
                self.assertEqual(response.status_code, 302)
                self.client.login(username='admin', password='admin')
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)
                self.assertFalse(response.context['user'].is_anonymous)
                self.assertTemplateUsed(
                    response, 'cabinet_app/product_delete.html')
                self.assertEquals(resolve(url).func.view_class,
                                  MyProductDeleteView)
                active = Product.objects.filter(
                    id=product.id).first().is_active
                self.client.post(url)
                active_finish = Product.objects.filter(
                    id=product.id).first().is_active
                self.assertNotEquals(active, active_finish)
                response = self.client.get(url)
                self.assertEqual(response.status_code, 404)
                self.client.logout()
            if product.is_active \
                    and product.category.is_active \
                    and product.company.is_active \
                    and product.company.company.is_active \
                    and product.company.company.username != 'admin':
                self.assertEqual(response.status_code, 302)
                self.client.login(username='admin', password='admin')
                response = self.client.get(url)
                self.assertEqual(response.status_code, 404)
                self.client.logout()
            elif (product.is_active == False
                  or product.category.is_active == False
                  or product.company.is_active == False
                  or product.company.company.is_active == False) \
                 and product.company.company.username == 'admin':
                self.assertEqual(response.status_code, 302)
                self.client.login(username='admin', password='admin')
                response = self.client.get(url)
                self.assertEqual(response.status_code, 404)
                self.client.logout()
            else:
                response = self.client.get(url)
                self.assertEqual(response.status_code, 302)

    # def tearDown(self):
    #     call_command('sqlsequencereset', 'main_app', 'auth_app',
    #                  'about_app',
    #                  'cabinet_app', 'search_app')
