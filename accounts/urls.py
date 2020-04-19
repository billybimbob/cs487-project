from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('', views.login, name='login'), # main page
    path('signup/', views.new_account, name='signup'),
    path('guest/', views.guest, name='guest'),
    path('validate/', views.mem_validate, name='validate'),
    path('<int:pk>/', views.DetailsView.as_view(), name='details'),
]