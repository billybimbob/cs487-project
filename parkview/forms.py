from django import forms
from .models import License


class AddLicenseForm(forms.ModelForm):
    value = forms.CharField(max_length=7, label='Plate Number')

    class Meta:
        model = License
        fields = ['value']

