from django.db import models

# Create your models here.

# Choices for Enrollment Package
ENROLLMENT_PACKAGE = [
    ("----", "----"),
    ("FREE", "FREE"),
]


class EnrollmentAnswers(models.Model):
    email = models.EmailField()
    firstName = models.CharField(max_length=20, blank=True)
    middleName = models.CharField(max_length=20, blank=True)
    surname = models.CharField(max_length=20, blank=True)
    countryCode = models.CharField(max_length=5, blank=True)
    phoneNumber = models.CharField(max_length=15, blank=True)


    def __str__(self):
        return str(self.email)

