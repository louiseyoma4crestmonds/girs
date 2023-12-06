from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status

from .models import *
from as_plugin_conf import *
from .serializers import *
from api.serializers import UserProfileSerializer

import environ

# Initialise environment variables
ENV = environ.Env()
environ.Env.read_env()
# Create your views here.


@api_view(['POST'])
def register_free_user(request):
    serializer = UserProfileSerializer(data=request.data)
    valid_data = serializer.is_valid()
    if valid_data:


        userPassword = "XCABCZYXABCZCZ"



        if not APPLICATIONS_USER_MODEL.objects.filter(email=request.data['email']).exists():
            free_user = APPLICATIONS_USER_MODEL(
                email=request.data['email'],
                first_name=request.data['firstName'],
                middle_name=request.data['middleName'],
                last_name=request.data['surname'],
                mobile_number=request.data['countryCode'] +
                request.data['phoneNumber'],

            )
            free_user.set_password(userPassword)
            free_user.save()

            # email their login credentials
            email_context = {
                'email': free_user.email,
                'name': free_user.first_name,
                'password': userPassword,
                'domain': ENV('DOMAIN_PROTOCOL') + ENV('FRONTEND_DOMAIN_NAME')
            }
            try:
                send_email_to_user(free_user.email,
                                   email_context,
                                   "email/account_details.html",
                                   "email/account_details.txt"
                                   )
            except Exception as e:
                return Response({
                    "error": "Error sending email",
                    "code": 500
                })
        else:
            return Response({
                "status": "Account with email already exist",
                "code": 200,
            })

    return Response({
        "status": "success",
        "code": status.HTTP_201_CREATED,
    })


@api_view(['POST'])
def submit_enrollment_form(request):
    serializer = EnrollmentAnswersSerializer(data=request.data)

    valid_data = serializer.is_valid()

    if valid_data:
        enrollmentResponse = EnrollmentAnswers(
            email=request.data['email'],
            firstName=request.data['firstName'],
            middleName=request.data['middleName'],
            surname=request.data['surname'],
            phoneNumber=request.data['phoneNumber'],
            countryCode=request.data['countryCode'],
        )
        enrollmentResponse.save()
        return Response({
            "status": "success",
            "code": status.HTTP_201_CREATED,
        })
    else:
        return Response({'error': 'Invalid data'})
 