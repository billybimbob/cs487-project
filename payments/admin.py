from django.contrib import admin
from .models import CreditCard, Payment

# Register your models here.

class PaymentAdmin(admin.StackedInline):
    model = Payment
    extra = 3

admin.register(CreditCard)
admin.register(Payment, PaymentAdmin)