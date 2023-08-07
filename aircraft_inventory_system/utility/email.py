from django.core.mail import send_mail, EmailMessage, get_connection

from django.conf import settings


def send_mail(email, subject, message):
    subject = subject
    message = message
    print(message)
    email_from = settings.EMAIL_HOST_USER

    try:
        # send_mailjet_mail(email_from, email, subject, message)
        send_mail(subject, message, email_from, [email])

        return True
    except Exception as e:
        return False
