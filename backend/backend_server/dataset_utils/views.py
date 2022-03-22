from django.shortcuts import render
from django.http import JsonResponse

import json
# Create your views here.

def get_search_suggestions(request, currentInput):

    #print(currentInput)

    result = json.load(open('./datasets/search_suggestions.json'))
    print(len(result))

    newResult = []

    for location in result:
        #print('checking: ' + location.casefold() + ' against ' + currentInput.casefold())
        if (currentInput.casefold() in location.casefold()):
            newResult.append(location)

    return JsonResponse(
        {"result": newResult}
        )