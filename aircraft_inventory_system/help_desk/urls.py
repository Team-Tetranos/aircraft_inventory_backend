from django.urls import path
from .views import *
urlpatterns = [
    path('help-desk/', help_desks, name='helps'),

]