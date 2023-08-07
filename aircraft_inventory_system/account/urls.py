from django.urls import path
from .views import UserRegistrationView, UserLoginView, reset_password
urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('reset-password/', reset_password, name='reset-password'),
]