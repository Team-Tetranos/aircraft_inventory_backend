from django.shortcuts import render
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ProfileSerializer
from rest_framework.permissions import IsAuthenticated
from .models import Profile

from rest_framework.mixins import UpdateModelMixin, RetrieveModelMixin


# Create your views here.

class MyProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        try:
            serializer = ProfileSerializer(request.user)
            send_data = serializer.data
            send_data.update({'key': 'MY_PROFILE'})
            return Response(send_data,
                            status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': ErrorDetail(string=e), 'key': 'SERVER_ERROR'},
                            status=status.HTTP_400_BAD_REQUEST)


class ProfileUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(Profile, user=self.request.user)

    def get(self, request, *args, **kwargs):
        profile = self.get_object()
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        profile = self.get_object()
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            send_data = serializer.data
            send_data.update({'key': 'PROFILE_UPDATE_SUCCESSFULLY'})
            return Response(send_data,
                            status=status.HTTP_200_OK)
        return Response({'error': ErrorDetail(string=serializer.errors), 'key': 'SERVER_ERROR'},
                        status=status.HTTP_400_BAD_REQUEST)




