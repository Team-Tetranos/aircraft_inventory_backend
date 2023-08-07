from django.urls import path
from .views import MyProfileView, ProfileUpdateView, profile_detail_for_admin, all_profiles_for_admin, profile_verify_for_admin
urlpatterns = [
    path('my-profile/', MyProfileView.as_view(), name='my-profile'),
    path('update-profile/', ProfileUpdateView.as_view(), name='update-profile'),
    path('user-profile/<str:id>/', profile_detail_for_admin, name='user-profile'),
    path('all-profile/', all_profiles_for_admin, name='all-profile'),
    path('verify-profile/<str:id>/', profile_verify_for_admin, name='verify-profile'),
]