import uuid

from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from account.models import User
from aircraft.models import Aircraft
from django_mysql.models import ListTextField


# Create your models here.

class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)

    first_name = models.CharField(blank=True, null=True, max_length=100)
    last_name = models.CharField(blank=True, null=True, max_length=100)
    email = models.EmailField(blank=True, null=True, max_length=255)
    phone = models.CharField(blank=True, null=True, max_length=15)
    is_admin = models.BooleanField(blank=True, null=True, default=False)
    is_verified = models.BooleanField(blank=True, null=True, default=False)
    permitted_aircrafts = models.ManyToManyField(Aircraft, related_name='aircraft', null=True, blank=True)
    profile_image = models.ImageField(upload_to='assets/profile_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    print('Profile creating')
    if created:
        profile = Profile.objects.create(email=instance.email, is_admin=instance.is_superuser)
        print(profile.email)


@receiver(post_delete, sender=User)
def delete_profile(sender, instance, **kwargs):
    print('Profile creating')
    profile = Profile.objects.get(email=instance.email)
    profile.delete()

