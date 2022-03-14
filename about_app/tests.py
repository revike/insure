from django.core.management import call_command
from django.test import TestCase, Client
from django.urls import reverse, resolve

from about_app.views import ContactView, InformationView, PoliticsView, \
    CookieView, FeedbackView
from insure.settings import DATABASES


class TestAboutApp(TestCase):
    databases = DATABASES

    def setUp(self):
        call_command('flush', '--noinput')
        call_command('loaddata', 'test_db.json')
        self.client = Client()

    def test_contacts(self):
        url = reverse('about_app:contacts')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about_app/contacts.html')
        self.assertEquals(resolve(url).func.view_class, ContactView)

    def test_information(self):
        url = reverse('about_app:information')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about_app/information.html')
        self.assertEquals(resolve(url).func.view_class, InformationView)

    def test_politics(self):
        url = reverse('about_app:politics')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about_app/politics.html')
        self.assertEquals(resolve(url).func.view_class, PoliticsView)

    def test_cookies(self):
        url = reverse('about_app:cookie')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about_app/cookies.html')
        self.assertEquals(resolve(url).func.view_class, CookieView)

    def test_feedback(self):
        url = reverse('about_app:feedback')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about_app/feedback.html')
        self.assertEquals(resolve(url).func.view_class, FeedbackView)

    def test_feedback_form(self):
        url = reverse('about_app:feedback')

        data = {
            'name': 'test',
            'email': 'test@local.ru',
            'subject': 'test',
            'message': 'test',
        }

        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

