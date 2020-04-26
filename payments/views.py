from django.shortcuts import render

# Create your views here

def payment_page(request):

    return render(request, 'payments/payments.html', {'title': 'Payments'})