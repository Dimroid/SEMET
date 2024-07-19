# monitoring/forms.py

from django import forms
from .models import Appliance
from django.forms import modelformset_factory

class ApplianceForm(forms.ModelForm):
    class Meta:
        model = Appliance
        fields = ['name', 'hours_per_day']

# Create a formset for ApplianceForm
ApplianceFormSet = modelformset_factory(Appliance, form=ApplianceForm)
