from django.db import models
from accounts.models import User

# Create your models here.

class CreditCard(models.Model):
    user   = models.OneToOneField(User, on_delete=models.CASCADE)
    number = models.CharField(max_length=20, unique=True)
    cvv    = models.CharField(max_length=3)

    def __str__(self):
        return f'card {self.number} owned by {self.user}'


class Payment(models.Model):
    paid_by = models.ForeignKey(CreditCard, on_delete=models.PROTECT, related_name='payments')
    date    = models.TimeField(auto_now_add=True)
    amount  = models.IntegerField()

    def __str__(self):
        user = getattr(self.paid_by, 'user')
        return f'{self.amount} paid by {user} on {self.date}'