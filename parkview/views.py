from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.views import generic

from .models import ParkingGarage, ParkingSpot

# Create your views here.

def garages(request):
    return HttpResponse('these will be all the garages')

def spots(request, garage_id):
    garage = get_object_or_404(ParkingGarage, pk=garage_id)
    floors = [garage.spots.filter(floor=num) for num in range(garage.floors)]
    context = {'garage': garage, 'floors': floors}
    return render(request, 'parkview/spots.html', context)

def parkspot(request, spot_id):
    return HttpResponse(f'looking at id {spot_id}')

class GaragesView(generic.ListView):
    template_name = 'parkview/garages.html'
    context_object_name = 'nearby_garages'

    def get_queryset(self):
        """get the 10 closest garages"""
        # no loc calc right now
        return getattr(ParkingGarage, 'objects').all()[:10]

