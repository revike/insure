from django.core.management import call_command
from django.test import TestCase, Client

from auth_app.models import CompanyUser
from insure.settings import DATABASES


class TestAuthApp(TestCase):
    databases = DATABASES

    def setUp(self):
        call_command('flush', '--noinput')
        self.superuser = CompanyUser.objects.create_superuser(
            username='admin', email='admin@mail.local', password='pass',
            last_name='admin', first_name='admin', is_active=True)
        self.client = Client()

    def test_login(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_anonymous)

        response = self.client.get('/auth/login/')
        self.assertEqual(response.status_code, 200)

        self.client.login(username='admin', password='pass')

        self.assertFalse(response.context['user'].is_anonymous)
        self.assertTrue(response.context['user'].is_superuser)
