from django.urls import path
from . import views

app_name = 'parkview'
urlpatterns = [
    path('', views.GaragesView.as_view(), name='garages'),
    path('<int:garage_id>/', views.spots, name='spots'),
    path('<int:spot_id>/spot', views.parkspot, name='parkspot'),
    path('license/', views.add_license, name='license')
]