# Generated by Django 4.2.3 on 2023-08-01 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aircraft', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='aircraft',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='assets/aircraft/'),
        ),
        migrations.AddField(
            model_name='aircraftitem',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='assets/aircraft_item/'),
        ),
    ]
