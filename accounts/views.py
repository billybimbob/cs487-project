from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views import generic
from .models import Member, User
from .forms import * #keep eye on

# Create your views here.

def index(request):
    return HttpResponse(f'This will be the login to a user page')

def login(request):
    context = {
        'form': LoginForm(),
        'method': "get",
        'target': 'accounts:validate',
        'submit': 'Login',
    }
    return render(request, 'accounts/signin.html', context)

def new_account(request):
    context = {
        'form': MemberForm(),
        'method': "post",
        'target': 'validate',
        'submit': 'Sign Up'
    }
    return render(request, 'accounts/signin.html', context)

def mem_validate(request):
    if request.method == 'POST':
        pass
    else: #get
        pass
    return HttpResponse(f'check signin option')

def guest(request):
    context = {
        'form': GuestForm(),
        'method': "post",
        'target': 'guest_cont',
        'submit': 'Continue',
    }
    return render(request, 'accounts/signin.html', context)

def guest_signin(request):
    new_guest = User()
    new_guest.save()
    return HttpResponse(f'signed in as guest {new_guest.uid}')


def details(request, user_id):
    return HttpResponse(f'Member profile for {user_id}', user_id)

class DetailsView(generic.DetailView):
    model = Member