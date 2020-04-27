from django.db import models
from accounts.models import Customer
from creditcards.models import CardNumberField, CardExpiryField, SecurityCodeField
# Create your models here.

class CreditCard(models.Model):
    customer   = models.OneToOneField(Customer, on_delete=models.CASCADE)
    cc_name = models.CharField(max_length=50)
    cc_number = CardNumberField('card number')
    cc_expiry = CardExpiryField('expiration date')
    cc_code = SecurityCodeField('security code')

    def __str__(self):
        return f'Card: {self.cc_number}'


class Payment(models.Model):
    paid_by = models.ForeignKey(CreditCard, on_delete=models.PROTECT, related_name='payments')
    date    = models.TimeField(auto_now_add=True)
    amount  = models.IntegerField()

    def __str__(self):
        name = getattr(self.paid_by, 'cc_name')
        return f'{self.amount} paid by {name} on {self.date}'