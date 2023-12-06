from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth.models import Group
from .models import CrestlearnUser


User = get_user_model()


class GroupAdminForm(forms.ModelForm):
    class Meta:
        model = Group
        exclude = []

    # Add the users field
    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=False,
        # Use the pretty 'filter_horizontal widget'
        widget=FilteredSelectMultiple('users', False)
    )

    def __init__(self, *args, **kwargs):
        # Normal for initialization
        super(GroupAdminForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['users'].initial = self.instance.user_set.all()

    def save_m2m(self):
        self.instance.user_set.set(self.cleaned_data['users'])

    def save(self, *args, **kwargs):
        # Default save
        instance = super(GroupAdminForm, self).save()
        # Save many-to-many data
        self.save_m2m()
        return instance


class CrestlearnUserCreationForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Generate Random Password
        password = '2wq1@WQ!'
        # Set password and confirm password fields to the generated password
        self.fields["password1"].widget.attrs["value"] = password
        self.fields["password2"].widget.attrs["value"] = password

    class Meta(UserCreationForm):
        model = CrestlearnUser
        fields = ('email',)


class CrestlearnUserChangeForm(UserChangeForm):

    class Meta:
        model = CrestlearnUser
        fields = ('email',
                  'is_staff',
                  'is_active',
                  'is_first_time',
                  'last_name',
                  'middle_name',
                  'personal_email',
                  'mobile_number',

                  )



