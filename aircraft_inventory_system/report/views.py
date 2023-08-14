from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ErrorDetail
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ac_stock.models import StockRecord
from stock_history.models import StockHistory


# Create your views here.

@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Only superadmins can access these views
def get_all_report(request):
    try:
        if request.method == 'GET':
            send_data = []

            stocks = StockRecord.objects.all()
            ser = 1
            for stock in stocks:
                stock_dict = {}

                stock_dict['serial_no'] = ser
                stock_dict['part_no'] = stock.stock_no
                stock_dict['nomenclature'] = stock.description
                stock_dict['unit'] = stock.unit
                stock_dict['card_no'] = stock.card_no
                stock_dict['quantity'] = stock.balance
                stock_histories = StockHistory.objects.filter(stock_record__id=stock.id)




            # send_data.update({'key': 'STOCK_RECORD_FOR_AIRCRAFT'})
            return Response(send_data,
                            status=status.HTTP_200_OK)


    except Exception as e:
        print(e)
        return Response({'error': ErrorDetail(string='Server error'), 'key': 'SERVER_ERROR'},
                        status=status.HTTP_400_BAD_REQUEST)
