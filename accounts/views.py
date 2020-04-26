from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from .models import Customer
from .forms import UserSignupForm, UserUpdateForm, AddCreditCard
from django.contrib.auth.decorators import login_required

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
        if u_form.is_valid():
            u_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('/account-info')
    else:
        u_form = UserUpdateForm(instance=request.user)

    return render(request, 'accounts/account.html', {'u_form': u_form})


def account_spots(request):
    return render(request, 'accounts/spots.html', {'title':'Spots'})


def account_payments(request):
    if request.method == 'POST':
        add_form = AddCreditCard(request.POST, instance=request.user)
        if add_form.is_valid():
            credit_card = add_form.save(commit=False)
            credit_card.cid = request.user.customer
            credit_card.save()
            messages.success(request, f'Your card has been updated!')
            return redirect('/account-info')
    else: 
        add_form = AddCreditCard(instance=request.user)

    return render(request, 'accounts/payments.html', {'title':'Payments','form': add_form})
