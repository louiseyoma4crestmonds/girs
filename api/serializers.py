from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from .models import *



# User Serializer
class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        User = get_user_model()
        model = User
        fields = ['first_name',
                  'last_name',
                  'personal_email',
                  'mobile_number',
                  'email',
                  'is_first_time',

                  ]


# Serializer Sign-in data
class SigninSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    user_model = get_user_model()

    def validate(self, data):
        user = authenticate(**data)

        if user and user.is_active:
            # Reset users failed login attempt on successful credentials validation
            user.failed_login_attempts = 0
            user.save()
            return user
        else:
            # Check if submitted email exists
            # If it exists check if it's failed login attempt == 5
            email_owner_exists = self.user_model.objects.filter(
                email=data['email']).exists()
            if email_owner_exists:
                email_owner = self.user_model.objects.get(email=data['email'])
                email_owner.failed_login_attempts += 1
                email_owner.save()
        

# User Serializer
class TouristSitesSerializer(serializers.ModelSerializer):

    class Meta:
        model = TouristSites
        fields = "__all__" 