from django.shortcuts import render
import requests
from django.http import JsonResponse
from django.http import response

# Create your views here.
def getStuff(request, inputAddr):
    key = 'c7qYTGBjRaRkGF7ucqOvpNy6L1Q857oD'
    url = f'http://www.mapquestapi.com/geocoding/v1/address?key={key}&location={inputAddr}'
    r = requests.get(url)
    stuff = r.json()
    return JsonResponse(stuff)
