from django.urls import path
from .views import MyProfileView, ProfileUpdateView
urlpatterns = [
    path('my-profile/', MyProfileView.as_view(), name='my-profile'),
    path('update-profile/', ProfileUpdateView.as_view(), name='update-profile'),
]