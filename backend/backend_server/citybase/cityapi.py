from citybase.models import City
from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers
import sys

def getScores(request, city, state):
	cityQuery = City.objects.filter(state=state, city=city)
	if cityQuery.count() >= 2:
		sys.stderr.write(f"City {city}, {state} has 2 or more entries in the database!\n")
	city = serializers.serialize('python', city)[0]["fields"]
	response = {
		"city": city["name"],
		"state": city["state"],
		"safe-living-score": city["safelivingscore"],
		"latitude": city["latitude"],
		"longitude": city["longitude"],
		"population": city["population"],
		"crime-score": city["crimescore"],
		"property-crime-score": city["propertycrimescore"],
		"violent-crime-score": city["violentcrimescore"]
	}
	return JsonResponse(response)
