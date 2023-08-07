# Generated by Django 4.2.3 on 2023-08-06 20:21

from django.db import migrations, models
import django_mysql.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('first_name', models.CharField(blank=True, max_length=100, null=True)),
                ('last_name', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.EmailField(blank=True, max_length=255, null=True)),
                ('phone', models.CharField(blank=True, max_length=15, null=True)),
                ('is_admin', models.BooleanField(blank=True, default=False, null=True)),
                ('is_verified', models.BooleanField(blank=True, default=False, null=True)),
                ('aircrafts', django_mysql.models.ListTextField(models.CharField(max_length=300), blank=True, default=[], null=True, size=None)),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to='assets/profile_images/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
