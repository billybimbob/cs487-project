from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import login
from .models import Customer
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
            return redirect(reverse(account_info))
    else:
        form = UserSignupForm()
    return render(request, 'accounts/signup.html', {'form': form})

def account_info(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect(reverse(account_info))
    else:
        u_form = UserUpdateForm(instance=request.user)

    return render(request, 'accounts/account-info.html', {'u_form': u_form})
