from django.shortcuts import render
import requests
from django.http import JsonResponse

def getBoundaries(request, city, state):

    url = f'https://nominatim.openstreetmap.org/search.php?q={city}+{state}+united+states&polygon_geojson=1&format=json'
    r = requests.get(url)
    result = r.json()
    context = []
    p = 0
    for k2 in result:
        if 'boundary' in k2['class']:
            for k in k2['geojson']['coordinates'][1][0]:
                #context.append({})
                #context[p]["lat"] = k[0]
                #context[p]["lng"] = k[1]
                #p+=1

                context.append( [k[0],k[1]] )
    
    return JsonResponse(context, safe = False)