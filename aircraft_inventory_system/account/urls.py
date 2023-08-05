from django.urls import path
from .views import UserRegistrationView, UserLoginView, reset_password, user_detail
urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('reset-password/', reset_password, name='reset-password'),
    path('user-details/<str:id>/', user_detail, name='user-detail'),
]