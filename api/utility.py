# This package contains functions for performing operations that are performed regularly
from django.conf import settings
import os
import json

import boto3
from botocore.exceptions import ClientError
from django.core.exceptions import ObjectDoesNotExist

from knox.models import AuthToken

from api.models import *


def handle_uploaded_file(file, user_email, file_type):
    if file_type == 'profile_image':
        # Create a directory in media folder named profile_image if it doesnt exist
        if not os.path.exists(os.path.join(settings.MEDIA_ROOT, 'profile_image')):
            os.makedirs(os.path.join(settings.MEDIA_ROOT, 'profile_image'))

        # Save file to media/profile_image directory
        image_file = os.path.join(
            settings.MEDIA_ROOT, 'profile_image/' + user_email + '.png')
        with open(image_file, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
    return (image_file)


def delete_media_file(file_er):
    if os.path.isfile(file_er):
        os.remove(file_er)
        return ("Success")
    else:
        print('is not file')
    """
    try:
        os.remove(file)
    except FileNotFoundError:
        print("File not found")
    """

# Convert queryset to python dictionary


def to_python_obj(queryset):
    # Convert Queryset to python dictionary
    dictionary_of_items = [item for item in queryset]
    return (dictionary_of_items)


def send_email(
    recipient_email,
    email_subject,
    email_body_text,
    email_html_body
):
    # This address must be verified with Amazon SES.
    SENDER = "GIRS <admin@example>"

    # If your aws ses account is still in the sandbox, this address must be verified.
    RECIPIENT = recipient_email

    # Specify a configuration set. If you do not want to use a configuration
    # set, comment the following variable, and the
    # ConfigurationSetName=CONFIGURATION_SET argument below.
    # CONFIGURATION_SET = "ConfigSet"

    # If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
    AWS_REGION = "eu-west-2"

    # The subject line for the email.
    SUBJECT = email_subject

    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = (email_body_text
                 )

    # The HTML body of the email.
    BODY_HTML = email_html_body

    # The character encoding for the email.
    CHARSET = "UTF-8"

    # Create a new SES resource and specify a region.
    client = boto3.client('ses', region_name=AWS_REGION)

    # Try to send the email.
    try:
        # Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
            # If you are not using a configuration set, comment or delete the
            # following line
            # ConfigurationSetName=CONFIGURATION_SET,
        )
    # Display an error if something goes wrong.
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])




