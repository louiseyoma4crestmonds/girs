# All global imports for this file goes in this section(all procedures that..
# are used more than once go here)
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import Group

##############################################################################



"""
1.) Replace 'account' with the name of the django application
    that houses the user model.
2.) Replace 'CustomUser' with the name of the user model 
    of the destination application.
"""
from api.models import CrestlearnUser

APPLICATIONS_USER_MODEL = CrestlearnUser



"""
Access this function from any application or any where in the django project..
to get the group that the user belongs to whether 
BusinessAnalyst or ScrumMaster.
"""

def users_role(token):

    # get user instance
    current_user = get_token_user(
        token)
    
    # verify the group of the user
    users_group = Group.objects.get(user=current_user)

    return users_group.name



"""
Access this function from any application or any where in the django project..
to get a user instance tied to an authentication token.
"""
from knox.models import AuthToken

def get_token_user(token):
    try:
        token_user = AuthToken.objects.get(token_key=token)
    except ObjectDoesNotExist:
        return ("Invalid Token")
    else:
        token_user = APPLICATIONS_USER_MODEL.objects.get(email=token_user.user)

    return token_user