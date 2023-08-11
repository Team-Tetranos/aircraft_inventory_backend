import uuid

from django.db import models
from profiles.models import Profile
from ac_stock.models import StockRecord
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver


# Create your models here.

class StockHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    created_by = models.ForeignKey(Profile, on_delete=models.SET_NULL, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    stock_record = models.ForeignKey(StockRecord, on_delete=models.SET_NULL, blank=True, null=True)
    voucher_no = models.TextField(null=True, blank=True)
    quantity = models.IntegerField(default=0, blank=True, null=True)
    image = models.ImageField(upload_to='assets/stock_record_history/', blank=True, null=True)
    received = models.BooleanField(default=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.voucher_no}'


@receiver(post_save, sender=StockHistory)
def stock_history_saved(sender, instance, created, **kwargs):
    if created:
        stock = instance.stock_record

        if instance.received:
            stock.balance = stock.balance+instance.quantity

        else:
            stock.balance = stock.balance - instance.quantity
        stock.save()

        print(f"Task '{instance}' has been created.")
    else:
        stock = instance.stock_record
        if instance.received:
            stock.balance = stock.balance+instance.quantity
        else:
            stock.balance = stock.balance - instance.quantity

        stock.save()
        print(f"Task '{instance}' has been updated.")


@receiver(pre_delete, sender=StockHistory)
def stock_history_deleted(sender, instance, **kwargs):
    try:
        stock = instance.stock_record
        if instance.received:
            stock.balance = stock.balance - instance.quantity
        else:
            stock.balance = stock.balance + instance.quantity
        stock.save()
    except Exception as e:


        print(f"Task '{instance}' is being deleted.")
