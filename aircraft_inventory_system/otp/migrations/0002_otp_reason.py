# Generated by Django 4.2.3 on 2023-07-31 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('otp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='otp',
            name='reason',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
