from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.exceptions import ErrorDetail
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ProfileSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Profile

from rest_framework.mixins import UpdateModelMixin, RetrieveModelMixin

from aircraft.models import Aircraft

from utility.email import send_mail


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


@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated, IsAdminUser])  # Only superadmins can access these views
def profile_detail_for_admin(request, id):
    try:
        profile = get_object_or_404(Profile, id=id)

        if request.method == 'GET':
            serializer = ProfileSerializer(profile)
            send_data = serializer.data
            send_data.update({'key': 'PROFILE_DETAIL'})
            return Response(send_data,
                            status=status.HTTP_200_OK)

        elif request.method == 'POST':
            print(request.data)
            serializer = ProfileSerializer(profile, data=request.data)

            if serializer.is_valid(raise_exception=True):
                pf = serializer.save()
                f_air = []
                for aircrafts in request.data.get('permitted_aircrafts'):
                    try:
                        acft = Aircraft.objects.get(id=aircrafts.get('id'))
                        f_air.append(acft)
                    except Exception as e:
                        print(e)
                pf.permitted_aircrafts.set(f_air)

                send_data = serializer.data
                send_data.update({'key': 'PROFILE_UPDATED'})
                return Response(send_data,
                                status=status.HTTP_200_OK)
            return Response({'error': ErrorDetail(string='Profile update failed'),
                             'key': 'PROFILE_UPDATE_FAILED'},
                            status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            profile.delete()
            return Response({'key': 'PROFILE_DELETED'},
                            status=status.HTTP_200_OK)

    except Exception as e:
        print(e)
        return Response({'error': ErrorDetail(string='Server error'), 'key': 'SERVER_ERROR'},
                        status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])  # Only superadmins can access these views
def profile_verify_for_admin(request, id):
    try:

        if request.method == 'GET':
            print('verification is hit')
            profile = Profile.objects.get(id=id)
            profile.is_verified = True
            profile.save()
            send_mail(email=profile.email, subject="Account verification", message="Your account verification is completed, you can access our system")
            serializer = ProfileSerializer(profile)
            send_data = serializer.data
            send_data.update({'key': 'PROFILE_DETAIL'})
            return Response(send_data,
                            status=status.HTTP_200_OK)


    except Exception as e:
        print(e)
        return Response({'error': ErrorDetail(string='Server error'), 'key': 'SERVER_ERROR'},
                        status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])  # Only superadmins can access these views
def all_profiles_for_admin(request):
    try:
        if request.method == 'GET':
            me = request.user.email
            profile = Profile.objects.exclude(email=me)
            serializer = ProfileSerializer(profile, many=True)
            send_data = serializer.data
            # send_data.update({'key': 'ALL_PROFILES'})
            return Response(send_data,
                            status=status.HTTP_200_OK)


    except Exception as e:
        print(e)
        return Response({'error': ErrorDetail(string='Server error'), 'key': 'SERVER_ERROR'},
                        status=status.HTTP_400_BAD_REQUEST)
