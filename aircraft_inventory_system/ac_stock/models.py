import uuid

from django.db import models
from profiles.models import Profile
from aircraft.models import Aircraft


# Create your models here.
class StockRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    created_by = models.ForeignKey(Profile, on_delete=models.SET_NULL, blank=True, null=True)
    card_no = models.CharField(max_length=300, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    aircraft = models.ForeignKey(Aircraft, on_delete=models.SET_NULL, blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    unit = models.CharField(max_length=300, null=True, blank=True)
    stock_no = models.CharField(max_length=300, blank=True, null=True)
    balance = models.IntegerField(default=0, blank=True, null=True)
    location = models.TextField(blank=True, null=True)
    latest_expiry = models.DateField(blank=True, null=True)
    demand_schedule = models.DateField(blank=True, null=True)
    image = models.ImageField(upload_to='assets/stock_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.description}-{self.aircraft.name}'

    def validate_stock_record_permission(self):
        if self.aircraft not in self.created_by.permitted_aircrafts.all():
            raise ValueError("The selected aircraft is not permitted for this profile.")

    def save(self, *args, **kwargs):
        if not self.created_by.is_admin:
            self.validate_stock_record_permission()
        super(StockRecord, self).save(*args, **kwargs)


