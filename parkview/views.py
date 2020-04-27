from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.views import generic

from accounts.models import Customer
from .models import ParkingGarage, ParkingSpot, License
from .forms import AddLicenseForm

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

def add_license(request):
    if request.method == 'POST':
        add_form = AddLicenseForm(request.POST)
        if add_form.is_valid():
            plate = License()
            print(request.user)
            if str(request.user) != 'AnonymousUser':
                plate.owner = request.user.customer
            else:
                customer = Customer()
                customer.save()
                plate.owner = customer

            plate.value = add_form.cleaned_data['value']
            plate.save()

            if request.user != 'AnonymousUser':
                return redirect('/account-payments')
            else:
                request.session['cid'] = plate.customer.cid
                return redirect('/payments/payment')
    else: 
        add_form = AddLicenseForm()

    context = {
        'title': 'Payments',
        'form': add_form,
    }

    return render(request, 'parkview/add-license.html', context)

class GaragesView(generic.ListView):
    template_name = 'parkview/garages.html'
    context_object_name = 'nearby_garages'

    def get_queryset(self):
        """get the 10 closest garages"""
        # no loc calc right now
        return getattr(ParkingGarage, 'objects').all()[:10]

