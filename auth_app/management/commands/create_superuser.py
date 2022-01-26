from django.core.management import BaseCommand

from auth_app.models import CompanyUser


class Command(BaseCommand):
    """Команда для создания супер юзера"""

    def handle(self, *args, **options):
        CompanyUser.objects.filter(is_staff=True, is_superuser=True).delete()
        CompanyUser.objects.create_superuser('admin', 'admin@admin.local',
                                             'admin')
