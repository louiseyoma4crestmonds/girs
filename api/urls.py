from knox import views as knox_views
from .views import *
from . import views
from django.urls import include, path

urlpatterns = [
    path('login', SignIn.as_view(), name='login'),
    path('logoutall', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('logout/<str:email>', logout_all),
    path('password_reset', include(
        'django_rest_passwordreset.urls', namespace='password_reset')),
    path('validate_password_reset_token/<str:token>',
         ValidatePasswordResetToken.as_view(), name='validate_password_reset_token'),
    path('set_new_password', SetNewPassword.as_view(), name='set_new_password'),
    path('change_password', ChangePasswordView.as_view(), name='change_password'),
    path('update_password', UpdatePassword.as_view(), name='update_password'),
    path('user/<str:email>', get_user),
    path('account/verify/<str:email>', account_exists),
    path('tourist/sites', get_tourist_sites),



]
