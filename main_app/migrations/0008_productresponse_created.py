# Generated by Django 4.0.1 on 2022-03-06 13:56

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0007_alter_productoption_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='productresponse',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='создан'),
            preserve_default=False,
        ),
    ]
