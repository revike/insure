# Generated by Django 4.0.1 on 2022-01-27 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0002_alter_companyuserprofile_company'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='companyuserprofile',
            options={'verbose_name': 'профиль компании', 'verbose_name_plural': 'профили компаний'},
        ),
        migrations.AddField(
            model_name='companyuserprofile',
            name='label',
            field=models.ImageField(blank=True, upload_to='company_labels', verbose_name='лейбл'),
        ),
    ]
