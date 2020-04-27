from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from .models import Customer
from payments.models import CreditCard
from .forms import UserSignupForm, UserUpdateForm
from payments.forms import AddCreditCard
from django.contrib.auth.decorators import login_required
from parkview.forms import AddLicenseForm
from parkview.models import License

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
def account_info(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        l_form = AddLicenseForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('/account-info')
        if l_form.is_valid():
            plate = License(value=l_form.cleaned_data['value'], owner=request.user.customer)
            plate.save()
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
    if request.method == 'POST':
        add_form = AddCreditCard(request.POST, instance=request.user)
        if add_form.is_valid():
            credit_card = CreditCard()
            credit_card.customer = request.user.customer
            credit_card.cc_name = add_form.cleaned_data['cc_name']
            credit_card.cc_number = add_form.cleaned_data['cc_number']
            credit_card.cc_expiry = add_form.cleaned_data['cc_expiry']
            credit_card.cc_code = add_form.cleaned_data['cc_code']
            credit_card.save()
            messages.success(request, f'Your card has been added!')
            return redirect('/account-payments')
    else: 
        add_form = AddCreditCard(instance=request.user)

    context = {
        'title': 'Payments',
        'cards': CreditCard.objects.filter(customer=request.user.customer),
        'form': add_form
    }

    return render(request, 'accounts/payments.html', context)
