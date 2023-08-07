from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ErrorDetail
from rest_framework.response import Response
from .serializers import AircraftSerializer, AircraftItemSerializer
from rest_framework.permissions import IsAuthenticated
from .models import Aircraft, AircraftItem
from profiles.models import Profile


# Create your views here.

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_aircraft(request):
    if request.method == 'POST':
        try:
            serializer = AircraftSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                send_data = serializer.data
                send_data.update({'key': 'AIRCRAFT_CREATED'})
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
@permission_classes([IsAuthenticated])
def all_aircraft(request):
    if request.method == 'GET':
        try:
            if request.user.is_superuser:
                aircrafts = Aircraft.objects.all().order_by('-created_at')
                serializer = AircraftSerializer(aircrafts, many=True)
                send_data = serializer.data
                # send_data.update({'key': 'AIRCRAFT_CREATED'})
                return Response(send_data,
                                status=status.HTTP_200_OK)
            else:
                profile = Profile.objects.get(email=request.user.email)
                permitted_aircraft = profile.permitted_aircrafts.all()
                serializer = AircraftSerializer(permitted_aircraft, many=True)
                send_data = serializer.data
                # send_data.update({'key': 'AIRCRAFT_CREATED'})
                return Response(send_data,
                                status=status.HTTP_200_OK)


        except Exception as e:
            print(e)
            return Response({'error': ErrorDetail(string='Server error'), 'key': 'SERVER_ERROR'},
                            status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def permitted_aircraft(request):
#     if request.method == 'GET':
#         try:
#             if request.user.is_superuser:
#             aircrafts = Aircraft.objects.all().order_by('-created_at')
#             serializer = AircraftSerializer(aircrafts, many=True)
#             send_data = serializer.data
#             # send_data.update({'key': 'AIRCRAFT_CREATED'})
#             return Response(send_data,
#                             status=status.HTTP_200_OK)



        except Exception as e:
            print(e)
            return Response({'error': ErrorDetail(string='Server error'), 'key': 'SERVER_ERROR'},
                            status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_aircraft_item(request):
    if request.method == 'POST':
        try:
            serializer = AircraftItemSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                send_data = serializer.data
                send_data.update({'key': 'AIRCRAFT_CREATED'})
                return Response(send_data,
                                status=status.HTTP_201_CREATED)
            else:
                return Response(
                    {'error': ErrorDetail(string='Aircraft item is not created', ), 'key': 'SERIALIZATION_ERROR'},
                    status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(e)
            return Response({'error': ErrorDetail(string='Server error'), 'key': 'SERVER_ERROR'},
                            status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def all_aircraft_item(request):
    if request.method == 'GET':
        try:
            aircrafts = AircraftItem.objects.all()
            serializer = AircraftItemSerializer(aircrafts, many=True)
            send_data = serializer.data
            # send_data.update({'key': 'AIRCRAFT_CREATED'})
            return Response(send_data,
                            status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({'error': ErrorDetail(string='Server error'), 'key': 'SERVER_ERROR'},
                            status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def category_aircraft_item(request, id):
    if request.method == 'GET':
        try:
            aircrafts = AircraftItem.objects.filter(aircraft=id)
            serializer = AircraftItemSerializer(aircrafts, many=True)
            send_data = serializer.data
            # send_data.update({'key': 'AIRCRAFT_CREATED'})
            return Response(send_data,
                            status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({'error': ErrorDetail(string='Server error'), 'key': 'SERVER_ERROR'},
                            status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def aircraft_item_detail(request, id):
    try:
        aircraft_item = AircraftItem.objects.get(id=id)
    except AircraftItem.DoesNotExist:
        return Response(
            {'error': ErrorDetail(string='Aircraft item does not exist', ), 'key': 'AIRCRAFT_NOT_FOUND'},
            status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        serializer = AircraftItemSerializer(aircraft_item)
        send_data = serializer.data
        send_data.update({'key': 'AIRCRAFT_ITEM_DATA'})
        return Response(send_data,
                        status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = AircraftItemSerializer(aircraft_item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            send_data = serializer.data
            send_data.update({'key': 'AIRCRAFT_ITEM_DATA_UPDATED'})
            return Response(send_data,
                            status=status.HTTP_200_OK)

        return Response(
            {'error': ErrorDetail(string='Aircraft item is not updated', ), 'key': 'AIRCRAFT_NOT_UPDATED'},
            status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        aircraft_item.delete()
        return Response({'key': 'AIRCRAFT_ITEM_DELETED'},
                        status=status.HTTP_200_OK)
