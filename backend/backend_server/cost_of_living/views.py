from django.shortcuts import render
import requests
from django.http import JsonResponse
import json


# Numbeo api documentation : https://www.numbeo.com/api/doc.jsp

# Create your views here.
def getCostOfLiving(request, inputAddr):
    lon = float(lon)
    lat = float(lat)
    key = '6teph9uj3ztaa3'
    #url = f'/api/?api_key={key}&query={lon},{lat}&min_contributors=5&max_distance=10000'
    #cityName = 'Example'
    #state = 'Example'
    url = f'/api/city_prices?api_key={key}&query={inputAddr}'
    context = {
        'cost-of-living': 20
    }
    return JsonResponse(context)
