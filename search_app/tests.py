from django.core.management import call_command
from django.test import TestCase, Client
from django.urls import reverse, resolve

from insure.settings import DATABASES
from search_app.views import SearchView, FilterView


class TestSearchApp(TestCase):
    """Тесты поиска и фильтрации"""
    databases = DATABASES

    def setUp(self):
        call_command('flush', '--noinput')
        call_command('loaddata', 'test_db.json')
        self.client = Client()

    def test_search(self):
        """Тест поиска"""
        url = reverse('search_app:search')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search_app/search.html')
        self.assertEquals(resolve(url).func.view_class, SearchView)

    def test_filter(self):
        """Тест фильтрации"""
        url = reverse('search_app:filter')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search_app/search.html')
        self.assertEquals(resolve(url).func.view_class, FilterView)

    # def tearDown(self):
    #     call_command('sqlsequencereset', 'main_app', 'auth_app', 'about_app',
    #                  'cabinet_app', 'search_app')
