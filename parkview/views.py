from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic

from .models import ParkingGarage, ParkingSpot

# Create your views here.

def garages(request):
    return HttpResponse('these will be all the garages')

def spots(request, garage_id):
    return HttpResponse(f'parking spots for {garage_id}')


class GaragesView(generic.ListView):
    template_name = 'parkview/garages.html'
    context_object_name = 'nearby_garages'

    def get_queryset(self):
        """get the 10 closest garages"""
        # no loc calc right now
        return getattr(ParkingGarage, 'objects').all()[:10]


class SpotView(generic.DetailView):
    model = ParkingGarage
    template_name = 'parkview/spots.html'
