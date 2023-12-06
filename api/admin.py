from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from .forms import GroupAdminForm

from .models import *
from .forms import CrestlearnUserCreationForm, CrestlearnUserChangeForm

# Unregister the original Group admin.
admin.site.unregister(Group)

# Create a new Group admin.


class GroupAdmin(admin.ModelAdmin):
    # Use our custom form.
    form = GroupAdminForm
    # Filter permissions horizontal as well.
    filter_horizontal = ['permissions']


# Register the new Group ModelAdmin.
admin.site.register(Group, GroupAdmin)


class CrestlearnUserAdmin(UserAdmin):
    add_form = CrestlearnUserCreationForm
    form = CrestlearnUserChangeForm
    model = CrestlearnUser
    list_display = ('email',
                    'first_name',
                    'last_name',
                    'personal_email',
                    'is_staff',
                    'is_active',
                    'is_first_time',
                    
                    )
    list_filter = ('email', 'is_staff', 'is_active', 'is_first_time',)
    fieldsets = (
        (None, {'fields': ('password', 
         'failed_login_attempts', 'first_name', 'last_name', 'is_first_time',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_active', 'first_name', 'last_name')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)



admin.site.register(CrestlearnUser, CrestlearnUserAdmin)
admin.site.register(TouristSites)

