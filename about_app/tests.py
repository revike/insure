from django.core.management import call_command
from django.test import TestCase, Client
from django.urls import reverse, resolve

from about_app.forms import FeedBackForm
from about_app.views import ContactView, InformationView, PoliticsView, \
    CookieView, FeedbackView
from insure.settings import DATABASES
from captcha.conf import settings as captcha


class TestAboutApp(TestCase):
    """Тест приложения about_app"""
    databases = DATABASES

    def setUp(self):
        call_command('flush', '--noinput')
        call_command('loaddata', 'test_db.json')
        self.client = Client()

    def test_contacts(self):
        """Тест страницы контакты"""
        url = reverse('about_app:contacts')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about_app/contacts.html')
        self.assertEquals(resolve(url).func.view_class, ContactView)

    def test_information(self):
        """Тест страницы информации"""
        url = reverse('about_app:information')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about_app/information.html')
        self.assertEquals(resolve(url).func.view_class, InformationView)

    def test_politics(self):
        """Тест страницы политики конфиденциальности"""
        url = reverse('about_app:politics')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about_app/politics.html')
        self.assertEquals(resolve(url).func.view_class, PoliticsView)

    def test_cookies(self):
        """Тест страницы Cookie"""
        url = reverse('about_app:cookie')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about_app/cookies.html')
        self.assertEquals(resolve(url).func.view_class, CookieView)

    def test_feedback(self):
        """Тест обратной связи"""
        url = reverse('about_app:feedback')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about_app/feedback.html')
        self.assertEquals(resolve(url).func.view_class, FeedbackView)

    def test_feedback_form(self):
        """Тест формы обратной связи"""
        captcha.CAPTCHA_TEST_MODE = True
        url = reverse('about_app:feedback')

        data_true = {
            'user_name': 'test',
            'user_email': 'test@local.ru',
            'subject': 'test',
            'message': 'test',
            'Captcha_0': 'passed',
            'Captcha_1': 'passed',
        }

        data_false = {
            'user_name': 'test',
            'user_email': 'test@local',
            'subject': 'test',
            'message': 'test',
            'Captcha_0': 'passed',
            'Captcha_1': 'passed',
        }

        response = self.client.post(url, data=data_true)
        self.assertEqual(response.status_code, 302)

        form = FeedBackForm(data=data_true)
        self.assertTrue(form.is_valid())

        form = FeedBackForm(data=data_false)
        self.assertFalse(form.is_valid())

    # def tearDown(self):
    #     call_command('sqlsequencereset', 'main_app', 'auth_app', 'about_app',
    #                  'cabinet_app', 'search_app')
