import uuid

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from account.models import User


# Create your models here.

class Profile(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(blank=True, null=True, max_length=100)
    last_name = models.CharField(blank=True, null=True,max_length=100)
    email = models.EmailField(blank=True, null=True, max_length=255)
    phone = models.CharField(blank=True, null=True, max_length=15)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    print('Profile creating')
    if created:
        profile = Profile.objects.create(user=instance, email=instance.email)
        print(profile.email)
