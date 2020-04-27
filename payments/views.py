from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CreditCard, Payment
from .forms import AddCreditCard
from accounts.models import Customer

# Create your views here

def payment_page(request):
    if request.method == 'POST':
        add_form = AddCreditCard(request.POST)
        if add_form.is_valid():
            customer = Customer()
            customer.save()
            credit_card = CreditCard()
            credit_card.customer = customer
            credit_card.cc_name = add_form.cleaned_data['cc_name']
            credit_card.cc_number = add_form.cleaned_data['cc_number']
            credit_card.cc_expiry = add_form.cleaned_data['cc_expiry']
            credit_card.cc_code = add_form.cleaned_data['cc_code']
            credit_card.save()
            payment = Payment()
            payment.paid_by = credit_card
            payment.amount = 0
            payment.save()
            messages.success(request, f'Your payment was successful')
            return redirect('/payments/payment-complete')
    else: 
        add_form = AddCreditCard()

    context = {
        'title': 'Payments',
        'form': add_form
    }

    return render(request, 'payments/payment.html', context)


def payment_complete(request):

    context = {
        'title': 'Payment Complete'
    }

    return render(request, 'payments/payment-complete.html', context)