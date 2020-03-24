from django import forms
from Locations.models import *

class newLocationForm(forms.Form):
    LOC_TYPES =( 
    (1, "Country"), 
    (2, "Region"), 
    (3, "Cluster"), 
    )
    locationType = forms.ChoiceField(label='Location Type', choices=LOC_TYPES)
    locationName = forms.CharField(label='Location Name', max_length=100)
    locationParent_country = forms.ChoiceField(label='Parent Country')
    locationParent_region = forms.ChoiceField(label='Parent Region')
    
    def __init__(self, *args,**kwargs):
        super(newLocationForm, self).__init__(*args, **kwargs)
        locationParent_country = [('-1', '----------')]
        locationParent_region = [('-1', '----------')]
        countryList = [(country.locationID, country.locationName) for country in Location.objects.filter(parentLocID = -1).order_by('locationName')]
        regionList = [(region.locationID, region.locationName) for region in Location.objects.filter(parentLocID__in= [country.locationID for country in Location.objects.filter(parentLocID = -1)]).order_by('locationName')]
        locationParent_country.extend(countryList)
        locationParent_region.extend(regionList)
        self.fields['locationParent_country'].choices = locationParent_country
        self.fields['locationParent_region'].choices = locationParent_region        
