from django.shortcuts import render
import requests
from django.http import JsonResponse

# Create your views here.
def getBoundaries(request, city, state, country):
    
        city = city.replace(" ", "+")
        state = state.replace(" ", "+")
        country = country.replace(" ", "+")
        
        key = ''
        url = f'https://https://nominatim.openstreetmap.org/search.php?q={city}+{state}+{country}&polygon_geojson=1&format=json'
        urlRequest = requests.get(url)
        data = urlRequest.json()
        context = {
            "boundaries": data["coordinates"]
        }
    
