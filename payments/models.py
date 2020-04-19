from django.db import models
from accounts.models import User

# Create your models here.

class Payment(models.Model):
    user   = models.ForeignKey(User, on_delete=models.PROTECT, related_name='payments')
    date   = models.TimeField(auto_now_add=True)
    amount = models.IntegerField()

    def __str__(self):
        return f'{self.amount} paid by {self.user} on {self.date}'