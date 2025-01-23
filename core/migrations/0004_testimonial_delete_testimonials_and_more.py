# Generated by Django 4.2 on 2025-01-22 22:48

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_testimonials_alter_category_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Testimonial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author_name', models.CharField(max_length=100, verbose_name='author name')),
                ('author_title', models.CharField(blank=True, max_length=100, null=True, verbose_name='author title')),
                ('author_image', models.ImageField(blank=True, null=True, upload_to='testimonials/', verbose_name='author image')),
                ('content', models.TextField(verbose_name='content')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
            ],
            options={
                'verbose_name': 'testimonial',
                'verbose_name_plural': 'testimonials',
            },
        ),
        migrations.DeleteModel(
            name='Testimonials',
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'category', 'verbose_name_plural': 'categories'},
        ),
        migrations.AlterModelOptions(
            name='course',
            options={'verbose_name': 'course', 'verbose_name_plural': 'courses'},
        ),
        migrations.AddField(
            model_name='category',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2025, 1, 22, 22, 48, 37, 447082, tzinfo=datetime.timezone.utc), verbose_name='created at'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='category',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='updated at'),
        ),
        migrations.AddField(
            model_name='course',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2025, 1, 22, 22, 48, 51, 984543, tzinfo=datetime.timezone.utc), verbose_name='created at'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='course',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='updated at'),
        ),
        migrations.AlterField(
            model_name='course',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courses', to='core.category', verbose_name='category'),
        ),
        migrations.AlterField(
            model_name='course',
            name='is_popular',
            field=models.BooleanField(default=False, verbose_name='is popular'),
        ),
        migrations.AlterField(
            model_name='course',
            name='is_upcoming',
            field=models.BooleanField(default=False, verbose_name='is upcoming'),
        ),
    ]
