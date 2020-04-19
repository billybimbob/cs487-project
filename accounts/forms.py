from django import forms
from django.db import models

class GuestForm(forms.ModelForm): #has nothing right now
    pass

class LoginForm(forms.ModelForm):
    email    = forms.CharField(max_length=20)
    password = forms.CharField(max_length=20)

class MemberForm(forms.ModelForm):
    first_name = forms.CharField(max_length=20)
    last_name  = forms.CharField(max_length=128)
    email      = forms.CharField(max_length=20)
    password   = forms.CharField(max_length=20)

class TempLicensesForm(forms.ModelForm):
    pass