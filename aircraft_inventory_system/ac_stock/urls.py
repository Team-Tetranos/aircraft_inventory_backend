from django.urls import path
from .views import *

urlpatterns = [
    path('all-stock-records/', all_stock_record, name='all-stock-record'),
    path('stock-records-by/<str:id>/', get_stock_by_aircraft, name='stock-by-aircraft'),
    path('stock-records-by-id/<str:id>/', get_stock_by_id, name='stock-by-id'),
    path('create-stock-records/', create_stock, name='create-stock-record'),
]