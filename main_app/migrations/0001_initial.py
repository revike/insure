# Generated by Django 4.0.1 on 2022-01-26 10:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='название продукта')),
                ('short_desc', models.CharField(max_length=128, verbose_name='краткое описание')),
                ('description', models.TextField(blank=True, verbose_name='описание')),
                ('is_active', models.BooleanField(db_index=True, default=True, verbose_name='активна')),
            ],
            options={
                'verbose_name': 'продукты',
                'verbose_name_plural': 'продукты',
            },
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='название категории')),
                ('description', models.TextField(blank=True, verbose_name='описание')),
                ('is_active', models.BooleanField(db_index=True, default=True, verbose_name='активна')),
            ],
            options={
                'verbose_name': 'категории продуктов',
                'verbose_name_plural': 'категории продуктов',
            },
        ),
        migrations.CreateModel(
            name='ProductOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='цена')),
                ('term', models.IntegerField(verbose_name='срок в месяцах')),
                ('rate', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=4, verbose_name='процентная ставка')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.product', verbose_name='продукт')),
            ],
            options={
                'verbose_name': 'опции продукта',
                'verbose_name_plural': 'опции продукта',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.productcategory', verbose_name='категория'),
        ),
        migrations.AddField(
            model_name='product',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='компания'),
        ),
    ]
