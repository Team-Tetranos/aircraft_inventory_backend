from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ErrorDetail
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .models import StockRecord
from .serializers import StockRecordSerializer
from aircraft.models import Aircraft


# Create your views here.


@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Only superadmins can access these views
def create_stock(request):
    try:
        if request.method == 'POST':
            stock_serializer = StockRecordSerializer(data=request.data)
            if stock_serializer.is_valid():
                stock_serializer.save()
                send_data = stock_serializer.data
                send_data.update({'key': 'STOCK_RECORD_CREATED'})
                return Response(send_data,
                                status=status.HTTP_201_CREATED)
            else:
                return Response(
                    {'error': ErrorDetail(string='Aircraft is not created', ), 'key': 'SERIALIZATION_ERROR'},
                    status=status.HTTP_400_BAD_REQUEST)


    except Exception as e:
        print(e)
        return Response({'error': ErrorDetail(string='Server error'), 'key': 'SERVER_ERROR'},
                        status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Only superadmins can access these views
def get_stock_by_aircraft(request, id):
    try:
        if request.method == 'GET':
            stocks = StockRecord.objects.filter(aircraft__id=id)
            stock_serializer = StockRecordSerializer(stocks, many=True)
            send_data = stock_serializer.data
            # send_data.update({'key': 'STOCK_RECORD_FOR_AIRCRAFT'})
            return Response(send_data,
                            status=status.HTTP_200_OK)


    except Exception as e:
        print(e)
        return Response({'error': ErrorDetail(string='Server error'), 'key': 'SERVER_ERROR'},
                        status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])  # Only superadmins can access these views
def all_stock_record(request):
    print(request.user)
    try:
        if request.method == 'GET':
            stocks = StockRecord.objects.all()
            stock_serializer = StockRecordSerializer(stocks, many=True)
            send_data = stock_serializer.data
            #send_data.update({'key': 'STOCK_RECORD_FOR_AIRCRAFT'})
            return Response(send_data,
                            status=status.HTTP_200_OK)


    except Exception as e:
        print(e)
        return Response({'error': ErrorDetail(string='Server error'), 'key': 'SERVER_ERROR'},
                        status=status.HTTP_400_BAD_REQUEST)