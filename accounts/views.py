from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from payments.models import CreditCard, Payment
from payments.forms import AddCreditCard
from parkview.forms import AddLicenseForm
from parkview.models import License
from parkview.views import get_confirm_response

from .models import Customer, Member
from .forms import UserSignupForm, UserUpdateForm

def home(request):
    return render(request, 'accounts/home.html', {'title': 'Home'})

def signup(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            customer = Customer()
            customer.save()
            user.customer = customer
            user.save()
            messages.success(request, f'Your account has been created!')
            login(request, user)
            return redirect('/account-info')
    else:
        form = UserSignupForm()
    return render(request, 'accounts/signin.html', {'create_page': "active", 'form': form})

@login_required
def confirm_member(request):
    if hasattr(request.user, 'member'):
        return redirect('/account-info')

    elif request.method == 'POST':
        response = get_confirm_response(request)
        if response == 'confirm':
            try:
                credit_card = CreditCard.objects.get(customer=request.user.customer)
            except CreditCard.DoesNotExist:
                messages.warning(request, 'You must add a credit card')
                return redirect('/account-payments')
            
            member = Member(user=request.user)
            payment = Payment(paid_by=credit_card, amount=10) # 10 bucks
            member.save()
            payment.save()
            messages.success(request, 'Your membership was successfully created!')
        # cancel and success
        return redirect('/account-info')

    return render(request, 'accounts/member.html', {'user': request.user})

@login_required
def account_info(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        l_form = AddLicenseForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('/account-info')
        elif l_form.is_valid():
            plate = License(value=l_form.cleaned_data['value'], owner=request.user.customer)
            try:
                plate.save()
            except IntegrityError:
                messages.error(request, 'License already exists')
                return redirect('/account-info')

            messages.success(request, f'Your license plate has been updated!')
            return redirect('/account-info')
    else:
        u_form = UserUpdateForm(instance=request.user)
        l_form = AddLicenseForm(instance=request.user)

    context = {
        'u_form': u_form,
        'l_form': l_form,
        'plates': request.user.customer.licenses.all()
    }

    return render(request, 'accounts/account.html', context)


def account_spots(request):
    return render(request, 'accounts/spots.html', {'title':'Spots'})

@login_required
def account_payments(request):
    customer = request.user.customer
    try:
        credit_card = CreditCard.objects.get(customer=customer)
        have_card =True
    except CreditCard.DoesNotExist:
        have_card = False

    if request.method == 'POST':
        add_form = AddCreditCard(request.POST, instance=request.user)
        if add_form.is_valid():
            if not have_card: credit_card = CreditCard(customer=customer)
            
            credit_card.cc_name = add_form.cleaned_data['cc_name']
            credit_card.cc_number = add_form.cleaned_data['cc_number']
            credit_card.cc_expiry = add_form.cleaned_data['cc_expiry']
            credit_card.cc_code = add_form.cleaned_data['cc_code']
            credit_card.save()

            messages.success(request, f'Your card has been {"updated" if have_card else "added"}!')
            return redirect('/account-payments')
    else:
        add_form = AddCreditCard(instance=request.user)

    context = {'title': 'Payments', 'form': add_form}
    if have_card:
        context = {**context, **{'card': credit_card}}


    return render(request, 'accounts/payments.html', context)
