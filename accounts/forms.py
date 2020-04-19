from django import forms
from django.db import models
from .models import Member

class GuestForm(forms.Form): #has nothing right now
    pass

class LoginForm(forms.Form):
    email    = forms.CharField(max_length=20)
    password = forms.CharField(max_length=20)

class MemberForm(forms.ModelForm):
    class Meta:
        model  = Member
        fields = ['first_name', 'last_name', 'email', 'password']

class TempLicensesForm(forms.Form):
    pass