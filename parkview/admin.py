from django.contrib import admin
from .models import ParkingGarage, ParkingSpot
# Register your models here.

class SpotAdmin(admin.StackedInline):
    model = ParkingSpot
    extra = 3

admin.register(ParkingGarage)
admin.register(ParkingSpot, SpotAdmin)