# Imports from python library
from datetime import timedelta
import uuid
import json

# Imports from django's library
from django.http import JsonResponse
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist


# Imports from django_rest_framework
from rest_framework import generics, permissions, status
from django_rest_passwordreset.models import ResetPasswordToken
from django_rest_passwordreset.views import get_password_reset_token_expiry_time
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser

# Imports from third parties
from knox.models import AuthToken
from knox.auth import TokenAuthentication
import boto3

# Local Imports
from .serializers import *
from .models import *
from .utility import *
from as_plugin_conf import get_token_user
# from .forms import QuizForm, QuizQuestionForm, ActiveJourneyForm, LearningObjectiveForm

# Open and read configuration file for environment variables.
from django.conf import settings as conf_settings




class UpdatePassword(APIView):
    """
    An endpoint for updating password.
    """
    User = get_user_model()

    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        # Collect all requests data
        try:
            email = request.data['email']
            old_password = request.data['old_password']
            new_password = request.data['new_password']
        except KeyError:
            response = {
                'status': 'Failed',
                'code': status.HTTP_400_BAD_REQUEST,
                'message': 'Missing key or key values. email, old_password, new password expected'
            }
            return JsonResponse(response)

        # Retrieve user instance using email.
        try:
            current_user = self.User.objects.get(email=email)
        except ObjectDoesNotExist:
            response = {
                'status': 'Failed',
                'code': status.HTTP_400_BAD_REQUEST,
                'message': 'This is not a correct email for identifying a user account.'
            }
            return JsonResponse(response)

        # Check old password
        is_old_password = current_user.check_password(old_password)

        if is_old_password:
            # set_password also hashes the password that the user will get
            current_user.set_password(new_password)
            current_user.save()
            response = {
                'status': 'success',
                'code': status.HTTP_201_CREATED,
                'message': 'Password updated successfully'
            }
            return JsonResponse(response)
        else:
            response = {
                'status': 'Failed',
                'code': status.HTTP_400_BAD_REQUEST,
                'message': 'Wrong old_password'
            }
            return JsonResponse(response)


# Accepts email and password and then authenticates them
class SignIn(generics.GenericAPIView):
    serializer_class = SigninSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        # Get score of the user
        token = AuthToken.objects.create(user)[1]


        authenticated_user = {'email': user.email,
                              'first_name': user.first_name,
                              'middle_name': user.middle_name,
                              'last_name': user.last_name,
                              'personal_email': user.personal_email,
                              'mobile_number': user.mobile_number,
                              'is_first_time': user.is_first_time,
                              }

        # Initialize Response
        response = {
            'status': '',
            'code': '',
            'message': '',
            'data': []
        }

        response['data'] = [{"user": authenticated_user, "token": token}]
        response['status'] = 'Success'
        response['code'] = 200

        return JsonResponse(response)


class ValidatePasswordResetToken(generics.GenericAPIView):

    def get(self, request, token):
        token_status = 'valid'
        User = get_user_model()
        expiry_date = 0

        # get token validation time
        #password_reset_token_validation_time = get_password_reset_token_expiry_time()

        # find token
        reset_password_token = ResetPasswordToken.objects.filter(
            key=token).first()

        if reset_password_token is None:
            token_status = 'Invalid'
            return JsonResponse({"token_validity": token_status}, safe=False, status=status.HTTP_400_BAD_REQUEST)
        else:

            # check expiry date
            try:
                expiry_date = reset_password_token.created_at + \
                    timedelta(hours=get_password_reset_token_expiry_time())

                if timezone.now() > expiry_date:
                    # delete expired token
                    token_status = 'Expired'
                    reset_password_token.delete()
                    return JsonResponse({"token_validity": token_status}, safe=False, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                print(e)

        if token_status == 'valid':
            return JsonResponse({"token_validity": token_status, "token": token}, safe=False, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"token_validity": "Unknown"}, safe=False, status=status.HTTP_400_BAD_REQUEST)


class SetNewPassword(generics.GenericAPIView):

    def post(self, request):
        # find token
        reset_password_token = ResetPasswordToken.objects.filter(
            key=request.data['token']).first()
        if reset_password_token is not None:
            password_1 = request.data['password1']
            password_2 = request.data['password2']
            if password_1 == password_2:
                try:
                    User = get_user_model()
                    user = User.objects.get(email=reset_password_token.user)
                    user.set_password(password_1)
                    user.failed_login_attempts = 0
                    user.save()

                    # delete used token
                    reset_password_token.delete()
                except Exception as e:
                    print(e, 'this is an exception')
                    return JsonResponse({"password_is_reset": False, "message": "Token associated email not found"}, safe=False, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return JsonResponse({"password_is_reset": True}, safe=False, status=status.HTTP_201_CREATED)
            else:
                return JsonResponse({"password_is_reset": False, "message": "Password Mismatch"}, safe=False, status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse({"password_is_reset": False, "message": "Invalid Token"}, safe=False, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for updating password.
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        User = get_user_model()
        response = {}
        # set new password
        try:
            current_user = User.objects.get(email=request.data['email'])
            current_user.set_password(request.data['password'])
            current_user.save()

            # Check if its a first time user and if it is set is_first_time to False
            if current_user.is_first_time:
                current_user.is_first_time = False
                current_user.failed_login_attempts = 0
                current_user.save()

            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully'
            }
        except Exception as e:
            print(e)
            response = {
                'status': 'Failed',
                'code': status.HTTP_400_BAD_REQUEST,
                'message': 'Something went wrong! Password not updated'
            }
        return JsonResponse(response)


# Endpoint to get user details
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def get_user(request, email):

    # get user instance
    current_user = get_token_user(
        request.headers["Authorization"].split()[1][:8])
    
    try:
        print(current_user.email)
    except ObjectDoesNotExist:
        return Response({"error": "Invalid user email"})
    else:
        serialized_data = UserProfileSerializer(current_user, many=False)

        if serialized_data.is_valid:
            return Response({
                "status": "success",
                "code": status.HTTP_200_OK,
                "data": [serialized_data.data]
            }
            )

@api_view(['GET'])
def logout_all(request, email):
    user = CrestlearnUser.objects.get(email=email)
    tokens = AuthToken.objects.filter(user=user.id)
    for token in tokens:
        token.delete()

    return Response({
        "status": "success",
        "code": status.HTTP_200_OK,
        "data": "user"
    }
    )


# Endpoint to check account existence


@api_view(['GET'])
def account_exists(request, email):
    user_exists = CrestlearnUser.objects.filter(email=email).exists()

    return Response({
        "status": "success",
        "code": status.HTTP_200_OK,
        "data": user_exists
    }
    )


@api_view(['GET'])
def get_tourist_sites(request):
    serializer = TouristSitesSerializer(data=request.data)

    valid_data = serializer.is_valid()

    try:
        # Fetch videos of user based on specified status in url
        tourist_site = TouristSites.objects.all( )
    except Exception as e:
        return Response({"error": "e"})
    else:
        serialized_data = TouristSitesSerializer(
            tourist_site, many=True)

        if serialized_data.is_valid:
            return Response({
                "status": "success",
                "code": status.HTTP_200_OK,
                "data": [serialized_data.data]
            }
            )
 

