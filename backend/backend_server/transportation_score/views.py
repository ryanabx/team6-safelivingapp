from django.shortcuts import render
import requests
from django.http import JsonResponse

# Create your views here.

def getWalkScore(lon, lat, address):
    #IMPLEMENT THIS
    key = ''
    url = f'https://api.walkscore.com/score?format=json&address={address}&lat={lat}&lon={lon}&transit=0&bike=0&wsapikey={key}'
    r = requests.get(url)
    data = r.json()
    context = {
        "walkscore": data["walkscore"]
    }