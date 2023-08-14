from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ErrorDetail
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .models import StockRecord
from .serializers import StockRecordSerializer, StockHistorySerializerForReport, StockRecordSerializerForReport
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
            stocks = StockRecord.objects.filter(aircraft__id=id).order_by('-created_at')
            stock_serializer = StockRecordSerializer(stocks, many=True)
            send_data = stock_serializer.data
            # send_data.update({'key': 'STOCK_RECORD_FOR_AIRCRAFT'})
            return Response(send_data,
                            status=status.HTTP_200_OK)


    except Exception as e:
        print(e)
        return Response({'error': ErrorDetail(string='Server error'), 'key': 'SERVER_ERROR'},
                        status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])  # Only superadmins can access these views
def get_stock_by_id(request, id):
    try:
        stocks = StockRecord.objects.get(id=id)
        #print(request.data)
    except stocks.DoesNotExist:
        return Response(
            {'error': ErrorDetail(string='Stock Record does not exist', ), 'key': 'STOCK_NOT_FOUND'},
            status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        stock_serializer = StockRecordSerializer(stocks)
        send_data = stock_serializer.data
        send_data.update({'key': 'STOCK_RECORD'})
        return Response(send_data,
                        status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = StockRecordSerializer(stocks, data=request.data, partial=True)

        if serializer.is_valid():
            #print(serializer.data)
            serializer.save()
            send_data = serializer.data
            send_data.update({'key': 'STOCK_RECORD_UPDATED'})
            return Response(send_data,
                            status=status.HTTP_200_OK)

        return Response(
            {'error': ErrorDetail(string='STOCK_RECORD is not updated', ), 'key': 'STOCK_RECORD_NOT_UPDATED'},
            status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        stocks.delete()
        return Response({'key': 'STOCK_RECORD_DELETED'},
                        status=status.HTTP_200_OK)


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


@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Only superadmins can access these views
def stock_record_report(request):
    print(request.user)
    try:
        if request.method == 'GET':
            stocks = StockRecord.objects.all()
            stock_serializer = StockRecordSerializerForReport(stocks, many=True)
            send_data = stock_serializer.data

            return Response(send_data,
                            status=status.HTTP_200_OK)


    except Exception as e:
        print(e)
        return Response({'error': ErrorDetail(string='Server error'), 'key': 'SERVER_ERROR'},
                        status=status.HTTP_400_BAD_REQUEST)




