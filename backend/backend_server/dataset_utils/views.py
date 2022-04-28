from django.shortcuts import render
from django.http import JsonResponse

import json
# Create your views here.

def crime_data_wrapper():
    pass

def get_search_suggestions(request, currentInput):

    #print(currentInput)

    result = json.load(open('./datasets/us_city_info.json'))
    #print(len(result))

    cities = []
    newResult = []

    for location in result:
        #print('checking: ' + location.casefold() + ' against ' + currentInput.casefold())
        if (currentInput.casefold() in location['city'].casefold()):
            cities.append(location)

    cities.sort(key=lambda location: location['population'], reverse=True)
    for city in cities:
        newResult.append(city['city'] + ', ' + city['state_id'])

    return JsonResponse(
        {"result": newResult}
        )