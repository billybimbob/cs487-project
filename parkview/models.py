from django.db import models
from accounts.models import Customer

# Create your models here.

class License(models.Model):
    value = models.CharField(max_length=7, unique=True)
    owner = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='licenses')
    
    def __str__(self):
        return f'License {self.value} for {self.owner}'


class TempLicense(models.Model):
    plate  = models.OneToOneField(License, on_delete=models.CASCADE, related_name='temporary')
    expire = models.DateField()

    def __str__(self):
        return str(self.plate)


class ParkingGarage(models.Model):
    name     = models.CharField(max_length=30)
    street   = models.CharField(max_length=100)
    city     = models.CharField(max_length=100)
    country  = models.CharField(max_length=25)
    zip_code = models.IntegerField()
    floors   = models.IntegerField()

    def __str__(self):
        return f'{self.name} on {self.street} in {self.city}, {self.country}'


class ParkingSpot(models.Model):
    floor   = models.IntegerField(default=1)
    used_by = models.OneToOneField(License, on_delete=models.PROTECT, blank=True, null=True)
    garage  = models.ForeignKey(ParkingGarage, on_delete=models.PROTECT, related_name='spots')

    def user(self):
        return 'no one' if self.used_by is None \
          else self.used_by

    def __str__(self):
        return f'{self.garage.name} on floor {self.floor} used by {self.user()}'
