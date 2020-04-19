from django.db import models
from django.utils import timezone
from datetime import timedelta

# Create your models here.
    
class User(models.Model):
    uid = models.AutoField(primary_key=True)
    # check if guest with obj.member

    def __str__(self):
        return f'guest user {self.uid}' if not hasattr(self, 'member') \
        else   str(getattr(self, 'member'))

def after30days(cls):
    return timezone.now() + timedelta(days=30)

class Member(models.Model):
    user       = models.OneToOneField(User, on_delete=models.CASCADE, db_index=True)
    first_name = models.CharField(max_length=20)
    last_name  = models.CharField(max_length=128)
    email      = models.CharField(max_length=20, db_index=True)
    password   = models.CharField(max_length=20)
    start_date = models.DateField(auto_now_add=True)
    end_date   = models.DateField(default=after30days)

    def __str__(self):
        return f'member {self.first_name} {self.last_name}'


class License(models.Model):
    value = models.CharField(max_length=9, unique=True)
    owner = models.ForeignKey(Member, on_delete=models.PROTECT, related_name='licenses')
    
    def __str__(self):
        return f'temp license {self.value} for {self.owner}'


class TempLicense(models.Model):
    plate  = models.OneToOneField(License, on_delete=models.CASCADE, related_name='temporary')
    expire = models.DateField()

    def __str__(self):
        return str(self.plate)