from django.contrib import admin
from .models import Appliance, EnergyUsage

# Register your models here.
admin.site.register(Appliance)
admin.site.register(EnergyUsage)
