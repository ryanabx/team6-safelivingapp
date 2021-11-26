from django.shortcuts import render
import requests
from django.http import JsonResponse

# Create your views here.

def getAmenities(request, lat, lon, radius, type):
    lon = float(lon)
    lat = float(lat)
    radius = float(radius)
    key = 'd2a4876ac89f4c5c9bf85da882fb134f'
    url = f'https://api.geoapify.com/v2/places?categories=commercial&filter=circle:{lon},{lat},{radius}&limit=20&apiKey={key}'
    r = requests.get(url)
    return JsonResponse(r.json())