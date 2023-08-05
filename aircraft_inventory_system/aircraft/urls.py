from django.urls import path
from .views import create_aircraft, all_aircraft, create_aircraft_item, all_aircraft_item, category_aircraft_item, aircraft_item_detail
urlpatterns = [
    path('create-aircraft/', create_aircraft, name='create-aircraft'),
    path('all-aircraft/', all_aircraft, name='all-aircraft'),
    path('create-aircraft-item/', create_aircraft_item, name='create-aircraft-item'),
    path('all-aircraft-item/', all_aircraft_item, name='all-aircraft-item'),
    path('category-aircraft-item/<str:id>/', category_aircraft_item, name='category-aircraft-item'),
    path('aircraft-item/<str:id>/', aircraft_item_detail, name='aircraft-item-detail'),
]