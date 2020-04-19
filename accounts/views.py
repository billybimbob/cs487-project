from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def index(request):
    return HttpResponse(f'This will be the login to a user page')

def details(request, user_id):
    return HttpResponse(f'Member profile for {user_id}', user_id)