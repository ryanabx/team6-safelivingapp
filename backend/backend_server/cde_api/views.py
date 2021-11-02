from django.shortcuts import render
from django.views.generic import TemplateView
import requests
from django.http import JsonResponse

# Create your views here.
def getStuff(request, agency, fromDate, toDate):
    #agency = 'FL0500500'
    #fromDate = '2019'
    #toDate = '2020'
    if(toDate < fromDate):
        tempDate = fromDate
        fromDate = toDate
        toDate = tempDate
    if(toDate > 2020 or fromDate > 2020 or toDate < 2000 or fromDate < 2000):
        return_value = {
            'message': 'Please provide a valid date range (2000 to 2020)'
        }
        return JsonResponse(return_value)
    key = 'nHym62MTPDELS0XgtAZLLw0fL3jNWoNvsY2kn315'
    url = f'https://api.usa.gov/crime/fbi/sapi//api/summarized/agencies/{agency}/offenses/{fromDate}/{toDate}?api_key={key}'
    template_name = 'cdedata.html'
    r = requests.get(url)
    stuff = r.json()
    context = {
        'cdedata': r.json(),
        'yed': 'yeaaaa' 
    }
    #return render(request, template_name, context)
    return JsonResponse(stuff)