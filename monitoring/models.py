from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

def get_default_user():
    return User.objects.first().id  # or any other logic to get a default user

class Appliance(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default='Refrigerator')
    wattage = models.FloatField(help_text="Power usage in watts", null=True, blank=True)
    hours_per_day = models.FloatField(default=0, help_text="Usage hours per day")

    def daily_kwh(self):
        return (self.wattage * self.hours_per_day) / 1000 if self.wattage else 0

class EnergyUsage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    total_kwh = models.FloatField()

    def __str__(self):
        return f"{self.user.username} - {self.date} - {self.total_kwh} kWh"