from django.shortcuts import render
from django.template import loader
from django.http import JsonResponse
from .forms import *
from Questions import models
from Locations import models
from API import serializers
from django.forms.models import model_to_dict

def DashboardView(request):
    form = dashboardForm()
    incomplete = PatientAssessment.objects.filter(questionnaireStatus = "INCOMPLETE").count()
    incomplete_patients = PatientAssessment.objects.filter(questionnaireStatus = "INCOMPLETE").values()
    complete = PatientAssessment.objects.filter(questionnaireStatus = "COMPLETE").count()
    sizes = [complete, incomplete]
    labels = ['Completed Assessment', 'Unfinished Assessment']
    context = {
        'form': form,
        'sizes': sizes,
        'labels': labels,
        'incomplete_patients': incomplete_patients,
    }
    return render(request, 'dashboard.html', context)

"""
Purpose: Used in dashboard.js asynchronous AJAX call to retrieve direct children location (either Region/Cluster)
of the location chosen in dashboardForm (Dashboard/forms.py) choicefield. The database accessed is the Location Table

Request Parameters: parent location id
Returns: JSON object -> list of children's location IDs

Use: dashboard.js -> function observe()
"""
def ajaxLocation(request):
    locations_to_render = []
    location_id = request.GET.get('location_id')
    # location_type = request.GET.get('location_type')
    query_locations = Location.objects.filter(parentLocID = location_id)
    for loc in query_locations:
        locations_to_render.append(str(loc.locationID))
    return JsonResponse({'locations': locations_to_render})

"""
Purpose: Used in dashboard.js to retrieve complete & incomplete patient numbers used in chart.js 
based on the location specified in the Choicefield. The database accessed is the 
PatientAssessment table, HouseHold Table and Location Table (linked together through foreign keys)

Request Parameters: countryID, regionID, clusterID
Returns: JSON object -> a list of 2 elements: the first element is the number of COMPLETE assessments, 
the second element is a the number of INCOMPLETE assessments. 

Use: dashboard.js -> function get_data(countryID, regionID, clusterID)
"""
def ajaxData(request):
    countryID = request.GET.get('countryID')
    regionID = request.GET.get('regionID')
    clusterID = request.GET.get('clusterID')
    if clusterID != '0':
        incomplete = PatientAssessment.objects.filter(
            questionnaireStatus = "INCOMPLETE", 
            assess_patientID__householdID__parentLocID = int(clusterID)).count()
        complete = PatientAssessment.objects.filter(
            questionnaireStatus = "COMPLETE",
            assess_patientID__householdID__parentLocID = int(clusterID)).count()
    elif regionID != '0':
        incomplete = PatientAssessment.objects.filter(
            questionnaireStatus = "INCOMPLETE",
            assess_patientID__householdID__parentLocID__parentLocID = int(regionID)).count()
        complete = PatientAssessment.objects.filter(
            questionnaireStatus = "COMPLETE",
            assess_patientID__householdID__parentLocID__parentLocID = int(regionID)).count()       
    elif countryID != '0':
        incomplete = PatientAssessment.objects.filter(
            questionnaireStatus = "INCOMPLETE",
            assess_patientID__householdID__parentLocID__parentLocID__parentLocID = int(countryID)).count()
        complete = PatientAssessment.objects.filter(
            questionnaireStatus = "COMPLETE",
            assess_patientID__householdID__parentLocID__parentLocID__parentLocID = int(countryID)).count()
    elif countryID == '0':
        incomplete = PatientAssessment.objects.filter(questionnaireStatus = "INCOMPLETE").count()
        complete = PatientAssessment.objects.filter(questionnaireStatus = "COMPLETE").count() 
    return JsonResponse({'data': [complete, incomplete]})


"""
Purpose: Used in dashboard.js to retrieve incomplete patient data for the Incomplete Patient table. The database 
accessed is PatientAssesment Table, Questionnaire Table, Patient Table (linked through Foreign Keys)

Request Parameters: countryID, regionID, clusterID
Returns: JSON object -> a list of dicts that hold patient id, patient assessment start date, 
questionnaire name and questionnaire id of a single patient entity whose assessment status is "INCOMPLETE" and 
belongs to the specified location

JSON OBJECT RETURNED: {"data":[{},{},{}]}

Use: dashboard.js -> function get_patient_data(countryID, regionID, clusterID)
"""
def ajaxIncompletePatients(request):
    countryID = request.GET.get('countryID')
    regionID = request.GET.get('regionID')
    clusterID = request.GET.get('clusterID')
    if clusterID != '0':
        incomplete_patients = PatientAssessment.objects.filter(
            questionnaireStatus = "INCOMPLETE", 
            assess_patientID__householdID__parentLocID = int(clusterID)).select_related()
    elif regionID != '0':
        incomplete_patients = PatientAssessment.objects.filter(
            questionnaireStatus = "INCOMPLETE",
            assess_patientID__householdID__parentLocID__parentLocID = int(regionID)).select_related()
    elif countryID != '0':
        incomplete_patients = PatientAssessment.objects.filter(
                    questionnaireStatus = "INCOMPLETE",
                    assess_patientID__householdID__parentLocID__parentLocID__parentLocID = int(countryID)).select_related()
    elif countryID == '0':
        incomplete_patients = PatientAssessment.objects.filter(questionnaireStatus = "INCOMPLETE").select_related()
    data = []
    for patient in incomplete_patients:
        data.append({
            'patient_id' : patient.assess_patientID.patientID,
            'questionnaire_id': patient.assess_questionnaireID.questionnaireID,
            'questionnaire_name': patient.assess_questionnaireID.questionnaireName,
            'start': patient.start
        })
    return JsonResponse({'data':data})