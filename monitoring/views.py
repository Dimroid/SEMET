from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Appliance, EnergyUsage
from .forms import ApplianceForm
from .utils import get_appliance_wattage
from django.forms import modelformset_factory
from django.utils import timezone

@login_required
def add_appliance(request):
    ApplianceFormSet = modelformset_factory(Appliance, form=ApplianceForm, extra=1)

    if request.method == 'POST':
        formset = ApplianceFormSet(request.POST)
        if formset.is_valid():
            new_appliances = []
            for form in formset:
                if form.is_valid():
                    appliance = form.save(commit=False)
                    appliance.user = request.user
                    appliance.wattage = get_appliance_wattage(appliance.name)
                    appliance.save()
                    new_appliances.append(appliance)
            return redirect('monitoring:appliance_list')  # Redirect to appliance list after saving new appliances
    else:
        formset = ApplianceFormSet(queryset=Appliance.objects.none())
    
    return render(request, 'add_appliance.html', {'formset': formset})


@login_required
def appliance_list(request):
    appliances = Appliance.objects.filter(user=request.user).order_by('-id')[:1]  # Retrieve only the first appliance
    total_kwh = sum(appliance.daily_kwh() for appliance in appliances)
    return render(request, 'appliance_list.html', {'appliances': appliances, 'total_kwh': total_kwh})

def all_appliances(request):
    appliances = Appliance.objects.filter(user=request.user).order_by('-id')
    total_kwh = sum(appliance.daily_kwh() for appliance in appliances)
    return render(request, 'all_appliances.html', {'appliances': appliances, 'total_kwh': total_kwh})

@login_required
def energy_dashboard(request):
    appliances = Appliance.objects.filter(user=request.user)
    total_kwh = sum(appliance.daily_kwh() for appliance in appliances)
    
    # Check if an EnergyUsage object already exists for today
    today = timezone.now().date()
    if not EnergyUsage.objects.filter(user=request.user, date=today).exists():
        EnergyUsage.objects.create(user=request.user, total_kwh=total_kwh, date=today)
    
    usage_history = EnergyUsage.objects.filter(user=request.user).order_by('-date')
    
    return render(request, 'energy_dashboard.html', {
        'appliances': appliances,
        'total_kwh': total_kwh,
        'usage_history': usage_history
    })
