from django.core.management import BaseCommand

from auth_app.models import CompanyUser, CompanyUserProfile


class Command(BaseCommand):
    """Команда для создания супер юзера"""

    def handle(self, *args, **options):
        if not CompanyUser.objects.filter(is_staff=True, is_superuser=True):
            admin = CompanyUser.objects.create_superuser(
                'admin', 'admin@admin.local', 'admin')
            CompanyUserProfile.objects.create(
                company=admin, name='admin', tax_id=123, is_active=True)
