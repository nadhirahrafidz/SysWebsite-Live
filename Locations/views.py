from django.shortcuts import render, redirect 
from .forms import *
from Locations.models import *
from django.db.models import Max
from django.contrib.auth.decorators import user_passes_test

@user_passes_test(lambda u: u.is_superuser)
def createLocation(request):
    form = newLocationForm()
    if request.method == 'POST':
        form = newLocationForm(request.POST)
        if form.is_valid():
            locationType = form.cleaned_data['locationType']
            locationName = form.cleaned_data['locationName']
            next_id = int(Location.objects.aggregate(Max('locationID'))['locationID__max']) + 1 
            if locationType == "1":
                parentLocID = Location.objects.get(pk=-1)
                Location.objects.get_or_create(pk= next_id, locationName=locationName, parentLocID=parentLocID)
            elif locationType == "2":
                parentLocID = Location.objects.get(locationID=int(form.cleaned_data['locationParent_country']))
                Location.objects.get_or_create(pk= next_id, locationName=locationName, parentLocID=parentLocID)
            else:
                parentLocID = Location.objects.get(locationID=int(form.cleaned_data['locationParent_region']))
                Location.objects.get_or_create(pk= next_id, locationName=locationName, parentLocID=parentLocID)
            context={
                "location": locationName,
                "locationID": next_id
            }
            return render(request, 'successLocation.html', context)
    context = {
        "form": form
    }
    return render(request,'newLocation.html', context)
