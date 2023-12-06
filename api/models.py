import environ
import random
import string
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as lazy_text

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.conf import settings as conf_settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from django.core.mail import EmailMultiAlternatives

from datetime import datetime
from datetime import timedelta

from .managers import CustomUserManager
from .utility import send_email

from knox.models import AuthToken


# Initialise environment variables
ENV = environ.Env()
environ.Env.read_env()


# Custom user model, a subclass of the AbstractBaseUser


class CrestlearnUser(AbstractBaseUser, PermissionsMixin):

    # Define the initial subscription time for the platform user
    current_time = datetime.now()
    email = models.EmailField(lazy_text('Email Address'), unique=True)
    first_name = models.CharField(
        lazy_text('First Name'), max_length=50, default='')
    middle_name = models.CharField(
        lazy_text('Middle Name'), max_length=50, default='')
    last_name = models.CharField(
        lazy_text('Last Name'), max_length=50, default='')
    personal_email = models.EmailField(
        lazy_text('Personal Email Address'), max_length=50, default='')
    mobile_number = models.CharField(
        lazy_text('Mobile Number'), max_length=50, default='')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_first_time = models.BooleanField(default=True)
    failed_login_attempts = models.IntegerField(default=0)



    USERNAME_FIELD = 'email'
    #REQUIRED_FIELDS = ['']

    objects = CustomUserManager()

    def __str__(self):
        return self.email


"""
    Catch users post_save signal so that every user will have
    an automtically generated token that can be used for their initial login.
"""


@receiver(post_save, sender=conf_settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        
        # send an e-mail to the user
        password = ''.join(random.choice(string.ascii_uppercase)
                            for i in range(12))
        instance.set_password(password)
        instance.save()
        context = {
            'user_email': instance.email,
            'user_password': password,
            'user_firstname': instance.first_name,
            'site_url': str(ENV('DOMAIN_PROTOCOL')) + str(ENV('FRONTEND_DOMAIN_NAME'))
        }
        # render email text
        email_html_message = render_to_string(
            'email/account_creation.html', context)
        email_plaintext_message = render_to_string(
            'email/account_creation.txt', context)

        msg = EmailMultiAlternatives(
            # title:
            "{title} account created successfully".format(
                title="GIRS"),
            # message:
            email_plaintext_message,
            # from:
            "noreply@example.com",
            # to:
            [instance.email]
        )
        msg.attach_alternative(email_html_message, "text/html")
        msg.send()

        # Create initial authentication token so that first time login will be possible
        AuthToken.objects.create(user=instance)







class TouristSites(models.Model):
    place = models.CharField(max_length=255, default="Tourist Site", blank=False)
    longitude = models.CharField(max_length=255, default="0")
    latitude = models.CharField(max_length=255, default="0")



    def __str__(self):
        return str(self.place)