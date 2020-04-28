from django.shortcuts import get_object_or_404, render, redirect
from django.views import generic
from django.db import IntegrityError
from django.contrib import messages
from django.utils.datastructures import MultiValueDictKeyError

from accounts.models import Customer
from .models import ParkingGarage, ParkingSpot, License
from .forms import AddLicenseForm

# Create your views here.

def spots(request, garage_id):
    garage = get_object_or_404(ParkingGarage, pk=garage_id)
    floors = [garage.spots.filter(floor=num) for num in range(1,garage.floors+1)]
    context = {'garage': garage, 'floors': floors}
    return render(request, 'parkview/spots.html', context)

def get_confirm_response(request):
    try:
        response = request.POST['confirm'].lower()
    except MultiValueDictKeyError:
        response = 'cancel'
    return response

def parkspot(request, spot_id):
    spot = get_object_or_404(ParkingSpot, pk=spot_id)
    if request.method == 'POST':
        response = get_confirm_response(request)
        if response == 'confirm':
            request.session['spot'] = spot_id
            return redirect(f'/parkview/license')
        else:
            return redirect(f'/parkview/{spot.garage.id}')
            
    return render(request, 'parkview/spot-confirm.html', {'spot': spot})


def add_license(request):
    if request.method == 'POST':
        add_form = AddLicenseForm(request.POST)
        if add_form.is_valid():
            if str(request.user) != 'AnonymousUser':
                owner = request.user.customer
            else:
                customer = Customer()
                customer.save()
                owner = customer
                
            plate = License(value=add_form.cleaned_data['value'], owner=owner)
            try:
                plate.save()
            except IntegrityError:
                messages.error(request, 'License already exists')
                redirect('/account-info')
        else:
            try:
                license_id = request.POST['choice']
                plate = License.objects.filter(id=license_id).first()
            except MultiValueDictKeyError:
                messages.error(request, f'You must select a license.')
                return redirect('/parkview/license')

        request.session['plate'] = plate.id
        if str(request.user) == 'AnonymousUser':
            request.session['cid'] = plate.owner.cid

        return redirect('/payments/payment')

    add_form = AddLicenseForm()
    context = {
        'title': 'Payments',
        'form': add_form
    }
    if str(request.user) != 'AnonymousUser':
        licenses = request.user.customer.licenses.all()
        context = {**context, **{'licenses': licenses}}
    return render(request, 'parkview/add-license.html', context)


class GaragesView(generic.ListView):
    template_name = 'parkview/garages.html'
    context_object_name = 'nearby_garages'

    def get_queryset(self):
        """get the 10 closest garages"""
        # no loc calc right now
        return getattr(ParkingGarage, 'objects').all()[:10]

