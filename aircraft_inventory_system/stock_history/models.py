import uuid
from datetime import date

from django.db import models
from profiles.models import Profile
from ac_stock.models import StockRecord
from django.db.models.signals import post_save, pre_delete, post_delete, pre_save
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
    expire = models.DateField(blank=True, null=True)
    received = models.BooleanField(default=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.voucher_no}'


@receiver(post_save, sender=StockHistory)
def stock_history_saved(sender, instance, created, **kwargs):
    if created:
        stock = instance.stock_record
        total_balance = 0
        stock_histories = StockHistory.objects.filter(stock_record__id=stock.id)

        for s in stock_histories:
            if s.received:
                total_balance += s.quantity
            else:
                total_balance -= s.quantity
        stock.balance = total_balance

        closest_expiry = StockHistory.objects.filter(expire__gte=date.today()).order_by('expire').first()
        if closest_expiry and closest_expiry.expire >= date.today():
            stock.latest_expiry = closest_expiry.expire

        stock.save()
    else:
        stock = instance.stock_record
        total_balance = 0
        stock_histories = StockHistory.objects.filter(stock_record__id=stock.id)

        for s in stock_histories:
            if s.received:
                total_balance += s.quantity
            else:
                total_balance -= s.quantity

        print(total_balance)
        stock.balance = total_balance

        closest_expiry = StockHistory.objects.filter(expire__gte=date.today()).order_by('expire').first()
        if closest_expiry and closest_expiry.expire > date.today():
            stock.latest_expiry = closest_expiry.expire

        stock.save()

        print(f"Task '{instance}' has been created.")


# @receiver(pre_save, sender=StockHistory)
# def update_stock_balance(sender, instance, **kwargs):
#     try:
#         original_instance = sender.objects.get(id=instance.id)
#     except sender.DoesNotExist:
#         original_instance = None
#
#     if original_instance:
#         original_balance_change = original_instance.quantity if original_instance.received else -original_instance.quantity
#         instance.stock_record.balance -= original_balance_change
#
#     balance_change = instance.quantity if instance.received else -instance.quantity
#     instance.stock_record.balance += balance_change
#     instance.stock_record.save()


@receiver(post_delete, sender=StockHistory)
def stock_history_deleted(sender, instance, **kwargs):
    try:
        stock = instance.stock_record
        total_balance = 0
        stock_histories = StockHistory.objects.filter(stock_record__id=stock.id)

        for s in stock_histories:
            if s.received:
                total_balance += s.quantity
            else:
                total_balance -= s.quantity
        stock.balance = total_balance
        closest_expiry = StockHistory.objects.filter(expire__gte=date.today()).order_by('expire').first()
        if closest_expiry and closest_expiry.expire > date.today():
            stock.latest_expiry = closest_expiry.expire
        stock.save()
    except Exception as e:
        print(e)
