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

def addCity(city, state, safelivingscore, latitude, longitude, population, 
		crimescore, propertycrimescore, violentcrimescore):
	if city is None or state is None:
		sys.stderr.write(f"City and state name cannot be None.")
		return False
	if City.objects.filter(name=city, state=state).exists():
		sys.stderr.write(f"City {city}, {state} already exists!")
		return False
	city = City(name=city, state=state, safelivingscore=safelivingscore, latitude=latitude, longitude=longitude, population=population, crimescore=crimescore, propertycrimescore=propertycrimescore, violentcrimescore=violentcrimescore)
	city.save()
	return True

def delCity(city, state):
	cityQuery = City.objects.filter(name=city, state=state)
	if not cityQuery.exists():
		return False
	for city in cityQuery:
		city.delete()
	return True

def updateCity(city, state, safelivingscore=None, latitude=None, longitude=None, 
population=None, crimescore=None, propertycrimescore=None, violentcrimescore=None):
	if city is None or state is None:
		sys.stderr.write(f"City and state name cannot be None.")
		return False
	cityQuery = City.objects.filter(name=city, state=state)
	if not cityQuery.exists():
		return addCity(city, state, safelivingscore, latitude, longitude, population,
					crimescore, propertycrimescore, violentcrimescore)
	cities = list(cityQuery)
	if len(cities) >= 2:
		sys.stderr.write(f"City {city}, {state} has 2 or more entries in the database!\n")
		return False
	city = cities[0]
	if safelivingscore is not None:
		city.safelivingscore = safelivingscore
	if latitude is not None:
		city.latitude = latitude
	if longitude is not None:
		city.longitude = longitude
	if population is not None:
		city.population = population
	if crimescore is not None:
		city.crimescore = crimescore
	if propertycrimescore is not None:
		city.propertycrimescore = propertycrimescore
	if violentcrimescore is not None:
		city.violentcrimescore = violentcrimescore
	city.save()
	return True
	