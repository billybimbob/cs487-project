from django.db import models
from accounts.models import License

# Create your models here.

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