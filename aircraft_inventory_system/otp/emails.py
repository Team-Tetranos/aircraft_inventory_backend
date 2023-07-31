from django.core.mail import send_mail, EmailMessage, get_connection
from .models import Otp
import random
from django.conf import settings
from utility.mailjet_mail import send_mailjet_mail


def send_otp_via_mail(email):
    subject = f'Your account verification email'
    otp = random.randint(100000, 999999)
    message = f'Your otp is {otp}'
    print(message)
    email_from = settings.EMAIL_HOST_USER

    try:
        # send_mailjet_mail(email_from, email, subject, message)
        send_mail(subject, message, email_from, [email])
        otp_obj, created = Otp.objects.get_or_create(email=email)
        otp_obj.otp = otp
        otp_obj.save()
        return True
    except Exception as e:
        return False
