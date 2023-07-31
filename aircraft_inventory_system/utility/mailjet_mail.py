from django.conf import settings
from mailjet_rest import Client


def send_mailjet_mail(sender, receiver, subject, message):
    api_key = settings.MJ_API_KEY
    api_secret = settings.MJ_API_SECRET
    mailjet = Client(auth=(api_key, api_secret), version='v3.1')
    data = {
        'Messages': [
            {
                "From": {
                    "Email": f"{sender}",
                    "Name": "Me"
                },
                "To": [
                    {
                        "Email": f'{receiver}',
                        "Name": "You"
                    }
                ],
                "Subject": f'{subject}',
                "TextPart": f'{message}',
                "HTMLPart": ""
            }
        ]
    }
    result = mailjet.send.create(data=data)
    print(result.json())
    status_code = result.status_code
    if status_code == 200 or status_code == 201:
        return True
    else:
        return False
