from rest_framework import serializers
from .models import *


# Enrollment Answer Serializer
class EnrollmentAnswersSerializer(serializers.ModelSerializer):

    class Meta:
        model = EnrollmentAnswers
        fields = "__all__"

