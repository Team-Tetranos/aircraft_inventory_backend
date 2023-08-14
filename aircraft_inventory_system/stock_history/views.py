from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ErrorDetail
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from .models import StockHistory
from .serializers import StockHistorySerializer


# Create your views here.



@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])  # Only superadmins can access these views
def all_stock_History(request):

    try:
        if request.method == 'GET':
            stocks = StockHistory.objects.all()
            stock_serializer = StockHistorySerializer(stocks, many=True)
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
def get_stock_History_by_stock(request, id):

    try:
        if request.method == 'GET':
            stocks = StockHistory.objects.filter(stock_record__id=id).order_by('date')
            stock_serializer = StockHistorySerializer(stocks, many=True)
            send_data = stock_serializer.data
            #send_data.update({'key': 'STOCK_RECORD_FOR_AIRCRAFT'})
            return Response(send_data,
                            status=status.HTTP_200_OK)


    except Exception as e:
        print(e)
        return Response({'error': ErrorDetail(string='Server error'), 'key': 'SERVER_ERROR'},
                        status=status.HTTP_400_BAD_REQUEST)
@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Only superadmins can access these views
def create_stock_History(request):

    try:
        if request.method == 'POST':
            print(request.data)
            stock_serializer = StockHistorySerializer(data=request.data)
            if stock_serializer.is_valid(raise_exception=True):
                stock_serializer.save()
                send_data = stock_serializer.data
                send_data.update({'key': 'STOCK_HISTORY_CREATED'})
                return Response(send_data,
                                status=status.HTTP_201_CREATED)
            else:
                return Response(
                    {'error': ErrorDetail(string='Stock History is not created', ), 'key': 'SERIALIZATION_ERROR'},
                    status=status.HTTP_400_BAD_REQUEST)


    except Exception as e:
        print(e)
        return Response({'error': ErrorDetail(string='Server error'), 'key': 'SERVER_ERROR'},
                        status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Only superadmins can access these views
def create_bulk_stock_History(request):

    try:
        if request.method == 'POST':
            print(request.data)
            stock_serializer = StockHistorySerializer(data=request.data, many=True)
            if stock_serializer.is_valid(raise_exception=True):
                stock_serializer.save()
                send_data = stock_serializer.data
                send_data.update({'key': 'STOCK_HISTORY_CREATED'})
                return Response(send_data,
                                status=status.HTTP_201_CREATED)
            else:
                return Response(
                    {'error': ErrorDetail(string='Stock History is not created', ), 'key': 'SERIALIZATION_ERROR'},
                    status=status.HTTP_400_BAD_REQUEST)


    except Exception as e:
        print(e)
        return Response({'error': ErrorDetail(string='Server error'), 'key': 'SERVER_ERROR'},
                        status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])  # Only superadmins can access these views
def get_stock_history_by_id(request, id):
    try:
        stocks = StockHistory.objects.get(id=id)
        print(request.data)
    except stocks.DoesNotExist:
        return Response(
            {'error': ErrorDetail(string='Stock History does not exist', ), 'key': 'STOCK_HISTORY_NOT_FOUND'},
            status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        stock_serializer = StockHistorySerializer(stocks)
        send_data = stock_serializer.data
        send_data.update({'key': 'STOCK_HISTORY'})
        return Response(send_data,
                        status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = StockHistorySerializer(stocks, data=request.data, partial=True)

        if serializer.is_valid():
            #print(serializer.data)
            serializer.save()
            send_data = serializer.data
            send_data.update({'key': 'STOCK_HISTORY_UPDATED'})
            return Response(send_data,
                            status=status.HTTP_200_OK)

        return Response(
            {'error': ErrorDetail(string='STOCK_RECORD is not updated', ), 'key': 'STOCK_RECORD_NOT_UPDATED'},
            status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        stocks.delete()
        return Response({'key': 'STOCK_RECORD_DELETED'},
                        status=status.HTTP_200_OK)