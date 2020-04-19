from django.urls import path
from . import views

#app_name = 'accounts'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>', views.DetailsView.as_view(), name='details'),
]