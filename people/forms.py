from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm


from .models import Profile

class LoginForm(AuthenticationForm):
    """
    Custom login form for authentication, with a few bootstrap classes attached
    """
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        # Set some additional field attributes

        username_attrs = {
                'class': 'form-control',
                'id': 'lg_username',
                'placeholder': 'Your Username',
                'aria-label': 'Input for username',
                }
        self.fields['username'].widget.attrs.update(username_attrs)

        password_attrs = {
                'class':'form-control',
                'id': 'lg_password',
                'placeholder': 'Your Password',
                'aria-label': 'Input for password'
                }
        self.fields['password'].widget.attrs.update(password_attrs)


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('offline_name', 'email', 'bio', 'dob')
