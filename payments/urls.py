from django.urls import path
from . import views

app_name = 'payments'
urlpatterns = [
    path('payment/', views.payment_page, name='payment-page'),
    path('payment-complete/', views.payment_complete, name='payment-complete'),
]