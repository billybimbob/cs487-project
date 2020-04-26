from django.db import models
from accounts.models import Customer
from creditcards.models import CardNumberField, CardExpiryField, SecurityCodeField

# Create your models here.

class CreditCard(models.Model):
    cid   = models.OneToOneField(Customer, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    cc_number = CardNumberField(_('card number'))
    cc_expiry = CardExpiryField(_('expiration date'))
    cc_code = SecurityCodeField(_('security code'))

    def __str__(self):
        return f'Card: {self.cc_number}'


class Payment(models.Model):
    paid_by = models.ForeignKey(CreditCard, on_delete=models.PROTECT, related_name='payments')
    date    = models.TimeField(auto_now_add=True)
    amount  = models.IntegerField()

    def __str__(self):
        user = getattr(self.paid_by, 'user')
        return f'{self.amount} paid by {user} on {self.date}'