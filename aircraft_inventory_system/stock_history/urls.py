from django.urls import path
from .views import *

urlpatterns = [
    path('all-stock-history/', all_stock_History, name='all-stock-history'),
    path('create-stock-history/', create_stock_History, name='create-stock-history'),
    path('create-bulk-stock-history/', create_bulk_stock_History, name='create-bulk-stock-history'),
    path('stock-history-by-record/<str:id>/', get_stock_History_by_stock, name='stock-history-by-record'),
]