from django.core.management import BaseCommand

from main_app.models import ProductCategory


class Command(BaseCommand):
    """Команда для создания категорий"""

    def handle(self, *args, **options):
        if not ProductCategory.objects.filter(is_active=True):
            categories = ['Автострахование', 'Жизнь', 'Недвижимость']
            for category in categories:
                ProductCategory.objects.create(name=category, description='',
                                               is_active=True)
