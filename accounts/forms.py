from django import forms
from accounts.models import User
from payments.models import CreditCard
from django.contrib.auth.forms import UserCreationForm
from creditcards.forms import CardNumberField, CardExpiryField, SecurityCodeField


class UserSignupForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']

class AddCreditCard(forms.ModelForm):
    name = forms.CharField(label='Name on Card')
    cc_number = CardNumberField(label='Card Number')
    cc_expiry = CardExpiryField(label='Expiration Date')
    cc_code = SecurityCodeField(label='CVV/CVC')

    class Meta:
        model = CreditCard
        fields = ['name', 'cc_number', 'cc_expiry', 'cc_code']
