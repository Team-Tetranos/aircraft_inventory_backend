from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from account.models import User
from rest_framework.exceptions import ErrorDetail
from rest_framework.response import Response

from .emails import send_otp_via_mail

# Create your views here.


def validate_email(value):
    if User.objects.filter(email=value).exists():
        return False
    return True
@api_view(['POST'])
def send_otp(request):
    if request.method == 'POST':
        try:
            email = request.data.get('email')
            if validate_email(email):
                send_otp_via_mail(email)
                return Response({'message': 'Otp is sent successfully', 'key': 'OTP_SENT'},
                                status=status.HTTP_200_OK)
            else:
                return Response({'error': ErrorDetail(string='Email already exist'), 'key': 'DUPLICATE_EMAIL'},
                                status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(e)
            return Response({'error': ErrorDetail(string='Server error'), 'key': 'SERVER_ERROR'},
                            status=status.HTTP_400_BAD_REQUEST)