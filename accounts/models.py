from django.db import models

# Create your models here.
    
class User(models.Model):
    credit_card   = models.CharField(max_length=20, unique=True)
    license_plate = models.CharField(max_length=9)

    def __str__(self):
        return f'guest with plate: {self.license_plate}'

class Member(models.Model):
    user       = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=20)
    last_name  = models.CharField(max_length=256)
    email      = models.CharField(max_length=20)
    password   = models.CharField(max_length=20)
    start_date = models.DateField(auto_now_add=True)
    end_date   = models.DateField()

    def __str__(self):
        return f'member {self.first_name} {self.last_name}'
