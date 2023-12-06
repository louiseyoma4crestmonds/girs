from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.dispatch import receiver
from django.conf import settings as conf_settings


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param args:
    :param kwargs:
    :return:
    """

    # send an e-mail to the user
    context = {
        'frontend_domain': conf_settings.ENV('FRONTEND_DOMAIN_NAME'),
        'domain_protocol': conf_settings.ENV('DOMAIN_PROTOCOL'),
        'current_user': reset_password_token.user,
        'email': reset_password_token.user.email,
        'token': reset_password_token.key,
        'reset_password_url': "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)
    }

    # render email text
    email_html_message = render_to_string('email/password_reset.html', context)
    email_plaintext_message = render_to_string(
        'email/password_reset.txt', context)

    msg = EmailMultiAlternatives(
        # title:
        "Reset your {title} password".format(title="GIRS"),
        # message:
        email_plaintext_message,
        # from:
        "admin@example.com",
        # to:
        [reset_password_token.user.email]
    )
    msg.attach_alternative(email_html_message, "text/html")
    msg.send()
