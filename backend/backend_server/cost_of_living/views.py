from django.shortcuts import render
import requests
from django.http import JsonResponse
import json

# Create your views here.
def getCostOfLiving(request, lon, lat):
    lon = float(lon)
    lat = float(lat)
    key = ''
    url = f'/api/?api_key={key}&query={lon},{lat}&min_contributors=5&max_distance=10000'
    cityName = 'Example'
    state = 'Example'
    url = f'/api/city_prices?api_key={key}&query={cityName},%20{state}'
    context = {
        'cost-of-living': 20
    }
    return JsonResponse(context)
