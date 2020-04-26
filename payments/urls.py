from django.urls import path
from . import views

app_name = 'payments'
urlpatterns = [
    path('', views.payment_page, name='payments-page'),
]