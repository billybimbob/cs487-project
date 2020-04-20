from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views import generic
from .models import Member, User
from . import forms

# Create your views here.

def login(request):
    context = {
        'title': 'Parking Login',
        'login_page': "active",
        'form': forms.LoginForm(),
        'method': "get",
        'target': 'validate',
        'submit': 'Login',
    }
    return render(request, 'accounts/signin.html', context)

def new_account(request):
    context = {
        'title': 'Create a New Membership',
        'create_page': "active",
        'form': forms.MemberForm(),
        'method': "post",
        'target': 'validate',
        'submit': 'Sign Up'
    }
    return render(request, 'accounts/signin.html', context)

def mem_validate(request):
    mem = None
    if request.method == 'POST':
        form = forms.MemberForm(request.POST)
        if form.is_valid():
            user = User()
            user.save()
            mem = form.save()
            mem.user = user
            print('added new member')
    else: #get
        form = forms.LoginForm(request.GET)
        if form.is_valid():
            data = form.cleaned_data
            try:
                mem = getattr(Member, "objects").get(email=data["email"], password=data["password"])
            except getattr(Member, "DoesNotExist"):
                print('invalid credentials')

    if mem is not None:
        request.session['id'] = mem.user.uid
        print(f'successfully logged in as {request.session["id"]}')

    return HttpResponse(f'check signin option')

def guest(request):
    context = {
        'title': 'Guest Confirmation',
        'guest_page': "active",
        'form': forms.GuestForm(),
        'method': "post",
        'target': 'guest_cont',
        'submit': 'Continue',
    }
    return render(request, 'accounts/signin.html', context)

def guest_signin(request):
    new_guest = User()
    new_guest.save()
    request.session['id'] = new_guest.uid
    return HttpResponse(f'signed in as guest {new_guest.uid}')


def details(request, user_id):
    return HttpResponse(f'Member profile for {user_id}', user_id)

class DetailsView(generic.DetailView):
    model = Member