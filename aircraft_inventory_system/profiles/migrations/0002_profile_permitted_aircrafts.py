# Generated by Django 4.2.3 on 2023-08-06 22:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aircraft', '0004_auto_20230802_0103'),
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='permitted_aircrafts',
            field=models.ManyToManyField(blank=True, null=True, related_name='aircraft', to='aircraft.aircraft'),
        ),
    ]
