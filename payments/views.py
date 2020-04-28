from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import IntegrityError
from parkview.models import ParkingSpot, License
from accounts.models import Customer
from .models import CreditCard, Payment
from .forms import AddCreditCard

# Create your views here

def payment_page(request):
    if request.method == 'POST':
        add_form = AddCreditCard(request.POST)
        if add_form.is_valid():
            if str(request.user) != 'AnonymousUser':
                customer = request.user.customer
            else:
                customer = Customer.objects.get(cid=request.session['cid'])
            try:
                credit_card = CreditCard.objects.get(customer=customer)
            except CreditCard.DoesNotExist:
                credit_card = CreditCard(customer=customer)

            credit_card.cc_name = add_form.cleaned_data['cc_name']
            credit_card.cc_number = add_form.cleaned_data['cc_number']
            credit_card.cc_expiry = add_form.cleaned_data['cc_expiry']
            credit_card.cc_code = add_form.cleaned_data['cc_code']
            
        else: # guarantee customer as a credit card
            credit_card = CreditCard.objects.get(customer=request.user.customer)
 
        payment = Payment(paid_by=credit_card, amount=10)
        spot = ParkingSpot.objects.get(id=request.session['spot'])
        spot.used_by = License.objects.get(id=request.session['plate'])

        try:
            payment.save()
            spot.save()
        except IntegrityError:
            messages.error(request, 'License is already used')
            return redirect('/parkview/license/')

        messages.success(request, f'Your payment was successful')
        request.session['billing_name'] = credit_card.cc_name
        request.session['cc_number'] = credit_card.cc_number
        request.session['amount'] = payment.amount
        return redirect('/payments/payment-complete')

    # blank form
    add_form = AddCreditCard()
    context = {'title': 'Payments', 'form': add_form}

    if str(request.user) != 'AnonymousUser':
        try:
            credit_card = CreditCard.objects.get(customer=request.user.customer)
            context = {**context, **{'card': credit_card}}
        except CreditCard.DoesNotExist: #do not add to context
            pass

    return render(request, 'payments/payment.html', context)


def payment_complete(request):

    context = {
        'title': 'Payment Complete',
        'billing_name': request.session['billing_name'],
        'amount': request.session['amount'],
        'cc_number': request.session['cc_number'],
        'spot': ParkingSpot.objects.get(id=request.session['spot']),
        'plate': License.objects.get(id=request.session['plate'])
    }

    return render(request, 'payments/payment-complete.html', context)