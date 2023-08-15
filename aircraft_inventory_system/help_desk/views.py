from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ErrorDetail
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import *
from .serializers import *


# Create your views here.

@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Only superadmins can access these views
def help_desks(request):
    print(request.user)
    try:
        if request.method == 'GET':
            helps = HelpDesk.objects.all()
            helps_serializer = HelpDeskSerializer(helps, many=True)
            send_data = helps_serializer.data

            return Response(send_data,
                            status=status.HTTP_200_OK)


    except Exception as e:
        print(e)
        return Response({'error': ErrorDetail(string='Server error'), 'key': 'SERVER_ERROR'},
                        status=status.HTTP_400_BAD_REQUEST)
