from django.db import models
from accounts.models import Member

# Create your models here.

class License(models.Model):
    value = models.CharField(max_length=7, unique=True)
    owner = models.ForeignKey(Member, on_delete=models.PROTECT, related_name='licenses')
    
    def __str__(self):
        return f'temp license {self.value} for {self.owner}'


class TempLicense(models.Model):
    plate  = models.OneToOneField(License, on_delete=models.CASCADE, related_name='temporary')
    expire = models.DateField()

    def __str__(self):
        return str(self.plate)


class ParkingGarage(models.Model):
    block    = models.IntegerField()
    street   = models.CharField(max_length=100)
    city     = models.CharField(max_length=100)
    country  = models.CharField(max_length=25)
    zip_code = models.IntegerField()

    def __str__(self):
        return f'garage at {self.street} in {self.city}, {self.country}'


class ParkingSpot(models.Model):
    used_by = models.OneToOneField(License, on_delete=models.PROTECT, blank=True)
    garage  = models.ForeignKey(ParkingGarage, on_delete=models.PROTECT, related_name='spots')

    def __str__(self):
        user = 'no one' if self.used_by is None else self.used_by
        return f'parking spot {self.garage} used by {user}'
