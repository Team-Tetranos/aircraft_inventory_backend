# Generated by Django 4.2.3 on 2023-08-13 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ac_stock', '0002_stockrecord_demand_schedule_stockrecord_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='stockrecord',
            name='unit',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
