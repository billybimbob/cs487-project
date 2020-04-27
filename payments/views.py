from django.shortcuts import render, redirect
from django.contrib import messages
from parkview.models import ParkingSpot, License
from .models import CreditCard, Payment
from .forms import AddCreditCard
from accounts.models import Customer

# Create your views here

def payment_page(request):
    if request.method == 'POST':
        add_form = AddCreditCard(request.POST)
        try:
            if add_form.is_valid():
                credit_card = CreditCard()
                if str(request.user) != 'AnonymousUser':
                    credit_card.customer = request.user.customer
                else:
                    credit_card.customer = Customer.objects.filter(cid=request.session['cid']).first()

                credit_card.cc_name = add_form.cleaned_data['cc_name']
                credit_card.cc_number = add_form.cleaned_data['cc_number']
                credit_card.cc_expiry = add_form.cleaned_data['cc_expiry']
                credit_card.cc_code = add_form.cleaned_data['cc_code']
                credit_card.save()
                payment = Payment()
                payment.paid_by = credit_card
                payment.amount = 10
                payment.save()
                messages.success(request, f'Your payment was successful')

                request.session['billing_name'] = credit_card.cc_name
                request.session['cc_number'] = credit_card.cc_number
                request.session['amount'] = payment.amount

            else:
                credit_card = CreditCard.objects.filter(customer=request.user.customer).first() 

                request.session['billing_name'] = credit_card.cc_name
                request.session['cc_number'] = credit_card.cc_number

            return redirect('/payments/payment-complete')

        except Exception: #figure out actual exception
            messages.error(request, f'You must select a payment.')
            
    add_form = AddCreditCard()
    context = {
        'title': 'Payments',
        'form': add_form
    }
    if str(request.user) != 'AnonymousUser':
        context = {
            **{'cards': CreditCard.objects.filter(customer=request.user.customer)},
            **context
        } 

    return render(request, 'payments/payment.html', context)


def payment_complete(request):
    spot = ParkingSpot.objects.get(id=request.session['spot'])
    spot.used_by = License.objects.get(id=request.session['plate'])
    spot.save()
    context = {
        'title': 'Payment Complete',
        'billing_name': request.session['billing_name'],
        'amount': request.session['amount'],
        'cc_number': request.session['cc_number'],
        'spot': spot
    }

    return render(request, 'payments/payment-complete.html', context)