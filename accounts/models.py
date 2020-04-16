from django.db import models

# Create your models here.
    
class User(models.Model):
    credit_card   = models.CharField(max_length=20, primary_key=True)
    license_plate = models.CharField(max_length=9)

class Member(models.Model):
    user       = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=20)
    last_name  = models.CharField(max_length=256)
    start_date = models.DateField(auto_now_add=True)
    end_date   = models.DateField()
