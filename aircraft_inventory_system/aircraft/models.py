import uuid

from django.db import models


# Create your models here.
class Aircraft(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    aircraft_id = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='assets/aircraft/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}'


class AircraftItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    part_no = models.CharField(max_length=255, blank=True, null=True)
    nomenclature = models.CharField(max_length=255, blank=True, null=True)
    astronomical_unit = models.CharField(max_length=255, blank=True, null=True)
    card_no = models.CharField(max_length=255, blank=True, null=True)
    quantity = models.CharField(max_length=255, blank=True, null=True)
    received_di_org = models.CharField(max_length=255, blank=True, null=True)
    manufacturer = models.CharField(max_length=255, blank=True, null=True)
    expire = models.DateTimeField(blank=True, null=True)
    expenditure = models.CharField(blank=True, null=True, max_length=255)
    rmk = models.CharField(blank=True, null=True, max_length=255)
    aircraft = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='assets/aircraft_item/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.nomenclature}-{self.aircraft}'
