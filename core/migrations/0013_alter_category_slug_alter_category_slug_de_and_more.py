# Generated by Django 4.2 on 2025-02-04 23:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_category_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(blank=True, max_length=100, null=True, unique=True, verbose_name='slug'),
        ),
        migrations.AlterField(
            model_name='category',
            name='slug_de',
            field=models.SlugField(blank=True, max_length=100, null=True, unique=True, verbose_name='slug'),
        ),
        migrations.AlterField(
            model_name='category',
            name='slug_en',
            field=models.SlugField(blank=True, max_length=100, null=True, unique=True, verbose_name='slug'),
        ),
        migrations.AlterField(
            model_name='category',
            name='slug_fr',
            field=models.SlugField(blank=True, max_length=100, null=True, unique=True, verbose_name='slug'),
        ),
    ]
