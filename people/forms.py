from django import forms
from django.contrib.auth.models import User


from .models import Profile


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('offline_name', 'email', 'bio', 'dob')