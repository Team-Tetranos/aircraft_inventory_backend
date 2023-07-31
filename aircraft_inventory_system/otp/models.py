from django.db import models


# Create your models here.
class Otp(models.Model):
    email = models.EmailField(max_length=255, null=True, blank=True)
    otp = models.CharField(max_length=6, null=True, blank=True)
    reason = models.CharField(max_length=300, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.email}-{self.created_at}'
