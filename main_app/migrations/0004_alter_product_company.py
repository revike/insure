# Generated by Django 4.0.1 on 2022-01-28 11:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0003_alter_companyuserprofile_options_and_more'),
        ('main_app', '0003_alter_productresponse_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth_app.companyuserprofile', verbose_name='компания'),
        ),
    ]