from django import forms
from creditcards.forms import CardNumberField, CardExpiryField, SecurityCodeField
from .models import CreditCard


class AddCreditCard(forms.ModelForm):
    cc_name = forms.CharField(label='Name on Card')
    cc_number = CardNumberField(label='Card Number')
    cc_expiry = CardExpiryField(label='Expiration Date')
    cc_code = SecurityCodeField(label='CVV/CVC')

    class Meta:
        model = CreditCard
        fields = ['cc_name', 'cc_number', 'cc_expiry', 'cc_code']