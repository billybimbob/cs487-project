from django.contrib import admin
from .models import License, ParkingGarage, ParkingSpot
# Register your models here.

admin.site.register(License)
admin.site.register(ParkingGarage)
admin.site.register(ParkingSpot)