from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as lazy_text
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
import environ


# Initialise environment variables
ENV = environ.Env()
environ.Env.read_env()


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email address is the uniqie identifier 
    for authentication instead of username
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and generated_password
        """
        if not email:
            raise ValueError(lazy_text('Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(lazy_text('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(
                lazy_text('Superuser must have is_superuser=True'))
        return self.create_user(email, password, **extra_fields)
