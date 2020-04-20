from django import forms
from accounts.models import User
from django.contrib.auth.forms import UserCreationForm



class UserSignupForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']