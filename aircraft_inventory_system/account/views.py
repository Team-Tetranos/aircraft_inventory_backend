from account.models import User
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.serializers import ErrorDetail
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserRegistrationSerializer, UserLoginSerializer
from profiles.models import Profile
from profiles.serializers import ProfileSerializer
from otp.models import Otp

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def validate_email(value):
    if User.objects.filter(email=value).exists():
        return False
    return True

def match_otp(email, otp):
    try:
        otp_obj = Otp.objects.get(email=email)
        if otp_obj.otp == otp:
            return True
        else:
            return False
    except Exception as e:
        return False

# Create your views here.

class UserRegistrationView(APIView):
    def post(self, request, format=None):
        try:
            serializer = UserRegistrationSerializer(data=request.data)
            # if validate_email(request.data.get('email')) is False:
            #     return Response({'error': ErrorDetail(string='Email already exist'), 'key': 'DUPLICATE_EMAIL'},
            #                     status=status.HTTP_400_BAD_REQUEST)

            otp = request.data.get('otp')

            if not match_otp(request.data.get('email'), otp):
                return Response({'error': ErrorDetail(string='Does not match Otp'), 'key': 'OTP_MATCH_FAILED'},
                                status=status.HTTP_400_BAD_REQUEST)


            if serializer.is_valid(raise_exception=True):
                user = serializer.save()
                token = get_tokens_for_user(user=user)
                profile = Profile.objects.get(email=user.email)

                if profile is not None:
                    profile_serializer = ProfileSerializer(profile)
                    send_data = profile_serializer.data
                    send_data.update(token)
                    send_data.update({'key': 'USER_CREATED_WITH_PROFILE'})
                    return Response(send_data,
                                    status=status.HTTP_201_CREATED)

                else:
                    send_data = serializer.data
                    send_data.update(token)
                    send_data.update({'key': 'USER_CREATED_WITHOUT_PROFILE'})
                    return Response(send_data,
                                    status=status.HTTP_201_CREATED)
            return Response({'error': ErrorDetail(string='Validation Error', ), 'key': 'VALIDATION_ERROR'},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': ErrorDetail(string='Server error'), 'key': 'SERVER_ERROR'},
                            status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):

    def post(self, request, format=None):
        try:
            email = request.data.get('email')
            password = request.data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                serializer = UserLoginSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                profile = Profile.objects.get(email=user.email)
                if profile is not None:
                    profile_serializer = ProfileSerializer(profile)
                    token = get_tokens_for_user(user=user)
                    send_data = profile_serializer.data
                    send_data.update(token)
                    send_data.update({'key': 'MY_PROFILE'})
                    return Response(send_data,
                                    status=status.HTTP_200_OK)
                else:
                    token = get_tokens_for_user(user=user)
                    send_data = serializer.data
                    send_data.update(token)
                    send_data.update({'key': 'MY_USER'})
                    return Response(send_data,
                                    status=status.HTTP_200_OK)

            else:

                return Response({'error': ErrorDetail(string='Email or Password is not valid'),
                                 'key': 'VALIDATION_ERROR'},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': ErrorDetail(string='Server Error'), 'key': 'SERVER_ERROR'},
                            status=status.HTTP_400_BAD_REQUEST)
