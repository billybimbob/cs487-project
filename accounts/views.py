from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserSignupForm, UserUpdateForm

def home(request):
    return render(request, 'accounts/home.html', {'title': 'Home'})

def signup(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your account has been created! You are now able to log in.')
            return redirect('login')
    else:
        form = UserSignupForm()
    return render(request, 'accounts/signup.html', {'form': form})

def accountInfo(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('account-info')
    else:
        u_form = UserUpdateForm(instance=request.user)

    context = {
        'u_form': u_form,
    }

    return render(request, 'accounts/account-info.html', context)
