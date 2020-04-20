from django.contrib import admin
from .models import Member, User, License, TempLicense #Guest, 

# Register your models here.

#admin.site.register(Guest)
admin.site.register(Member)
admin.site.register(User)
admin.site.register(License)
admin.site.register(TempLicense)