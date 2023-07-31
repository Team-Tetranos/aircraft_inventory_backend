from django.core.mail import send_mail
from .models import Otp
import random
from django.conf import settings


def send_otp_via_mail(email):
    subject = f'Your account verification email'
    otp = random.randint(100000, 999999)
    message = f'Your otp is {otp}'
    print(message)
    emai_from = settings.EMAIL_HOST
    try:
        send_mail(subject, message, emai_from, [email])
    except Exception as e:
        print(e)
    user_obj = Otp.objects.get_or_create(email=email)
    user_obj.otp = otp
    user_obj.save()
