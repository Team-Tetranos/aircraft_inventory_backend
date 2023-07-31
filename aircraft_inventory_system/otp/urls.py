from django.urls import path
from .views import send_otp, verify_otp
urlpatterns = [
    path('send-otp/', send_otp, name='otp-send'),
    path('verify-otp/', verify_otp, name='verify-send')
]