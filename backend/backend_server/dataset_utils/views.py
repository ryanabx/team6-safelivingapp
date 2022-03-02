from django.shortcuts import render
from django.http import JsonResponse

import json
# Create your views here.

def get_search_suggestions(request):
    return JsonResponse(
        {"result": json.load(open('./datasets/search_suggestions.json'))}
        )