from django.core.management import call_command
from django.test import TestCase, Client
from django.urls import reverse, resolve

from auth_app.forms import CompanyUserLoginForm, CompanyUserRegisterForm
from auth_app.models import CompanyUser
from auth_app.views import LoginUserView, RegisterView
from insure.settings import DATABASES, DOMAIN_NAME
from captcha.conf import settings as captcha


class TestAuthApp(TestCase):
    """Тест проложения авторизации"""
    databases = DATABASES

    def setUp(self):
        call_command('flush', '--noinput')
        call_command('loaddata', 'test_db.json')
        self.user = CompanyUser.objects.create_user(
            username='user', email='user@local.su', password='pass',
            last_name='user', first_name='user', is_active=True)
        self.client = Client()

    def test_not_login(self):
        """Тест анонимного пользователя"""
        url = reverse('main_app:index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['title'], 'главная')
        self.assertTrue(response.context['user'].is_anonymous)

        url = reverse('auth_app:login')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'auth_app/login.html')
        self.assertEquals(resolve(url).func.view_class,
                          LoginUserView)

    def test_login(self):
        """Тест авторизации"""
        response = self.client.get(reverse('auth_app:login'))
        self.assertEqual(response.status_code, 200)
        self.client.login(username='user', password='pass')

        response = self.client.get(reverse('main_app:index'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['user'], self.user)
        self.assertFalse(response.context['user'].is_anonymous)

        response = self.client.get(reverse('auth_app:login'))
        self.assertEqual(response.status_code, 302)

    def test_logout(self):
        """Тест выхода с сайта (logout)"""
        response = self.client.get(reverse('main_app:index'))
        self.assertTrue(response.context['user'].is_anonymous)

        self.client.login(username='user', password='pass')
        response = self.client.get(reverse('main_app:index'))
        self.assertFalse(response.context['user'].is_anonymous)

        self.client.logout()
        response = self.client.get(reverse('main_app:index'))
        self.assertTrue(response.context['user'].is_anonymous)

    def test_register(self):
        """Тест регистрации"""
        captcha.CAPTCHA_TEST_MODE = True

        url = reverse('auth_app:register')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_anonymous)
        self.assertTemplateUsed(response, 'auth_app/register.html')
        self.assertEquals(resolve(url).func.view_class, RegisterView)

        data = {
            'username': 'test_1',
            'last_name': 'test_1',
            'first_name': 'test_1',
            'email': 'test_1@local.ru',
            'password1': '2vsh9kx2vsh9kx',
            'password2': '2vsh9kx2vsh9kx',
            'Captcha_0': 'passed',
            'Captcha_1': 'passed',
        }

        response = self.client.post(reverse('auth_app:register'), data=data)
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse('main_app:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_anonymous)

        user = CompanyUser.objects.get(username=data['username'])

        self.client.login(username=data['username'],
                          password=data['password1'])
        response = self.client.get(reverse('main_app:index'))
        self.assertTrue(response.context['user'].is_anonymous)

        activation_url = f'{DOMAIN_NAME}/auth/verify/' \
                         f'{user.email}/{user.activation_key}/'
        response = self.client.get(activation_url)
        self.assertEqual(response.status_code, 200)

        self.client.login(username=data['username'],
                          password=data['password1'])
        response = self.client.get(reverse('main_app:index'))
        self.assertFalse(response.context['user'].is_anonymous)

    def test_form_login(self):
        """Тест формы логирования"""
        data_true = {'username': 'user', 'password': 'pass'}
        data_false = {'username': 'user', 'password': 'password'}
        form = CompanyUserLoginForm(data=data_true)
        self.assertTrue(form.is_valid())
        form = CompanyUserLoginForm(data=data_false)
        self.assertFalse(form.is_valid())

    def test_form_register(self):
        """Тест формы регистрации"""
        captcha.CAPTCHA_TEST_MODE = True
        data_true = {
            'username': 'test_2',
            'last_name': 'test_2',
            'first_name': 'test_2',
            'email': 'test_2@local.ru',
            'password1': '2vsh9kx2vsh9kx',
            'password2': '2vsh9kx2vsh9kx',
            'Captcha_0': 'passed',
            'Captcha_1': 'passed',
        }
        form = CompanyUserRegisterForm(data=data_true)
        self.assertTrue(form.is_valid())
        data_false = {
            'username': 'test_3',
            'last_name': 'test_3',
            'first_name': 'test_3',
            'email': 'test_3@local.ru',
            'password1': '2vsh9kx2vsh9kx',
            'password2': '2vsh9kx2vsh9kx',
        }
        form = CompanyUserRegisterForm(data=data_false)
        self.assertFalse(form.is_valid())

    # def tearDown(self):
    #     call_command('sqlsequencereset', 'main_app', 'auth_app', 'about_app',
    #                  'cabinet_app', 'search_app')
