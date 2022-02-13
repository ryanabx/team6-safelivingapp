from math import sqrt
from django.shortcuts import render
import safe_living_score.views
from loc_to_addr.views import geocoding
from django.http import JsonResponse

import csv
import json
import requests
#csv.DictReader(file)

#TEST WITH: http://localhost:8000/recommendations/api/tulsa/4000/large



# PROTOTYPE REQUIREMENTS:

# GIVEN --> CITY, STATE, RADIUS, POPULATION SCALE
# RETURN --> CITY WITH HIGHEST SAFETY SCORE

def recommendCity(request, initialAddress, radiusValue, populationPreference="any"):
    return JsonResponse( recommend(initialAddress, radiusValue, populationPreference) )


def recommend(initialAddress, radiusValue, populationPreference="any"):

    startingCoordinates = getCoordinates(initialAddress)
    populationScale = getPopulationScale(populationPreference)
    radius = getRadius(radiusValue)

    cities = getCitiesOfPopulationInRange(startingCoordinates, populationScale, radius)

    maxScore = -1
    recommendedCity = None

    for city in cities: # Basic min/max calculation, but works (for now)
        print(city)
        curScore = getCrimeScore(city["city"], city["state_id"])
        print("curScore = ", curScore)
        
        if curScore >= maxScore:
            maxScore = curScore 
            recommendedCity = city
    
    if(recommendedCity == None):

        context = {
            "city" : "No City Found"
    }
    else:

        context = {
            #"recommendation" : ( "" + recommendedCity["city"] + ", " + recommendedCity["state"] )
            "city" : recommendedCity["city"],
            "state" : recommendedCity["state"],
            "population" : recommendedCity["population"],
            "Safe Living Score" : maxScore
        }
    
    return context




# TODO: Get long+lat of city, calling API

# GIVEN --> CITY NAME AND STATE NAME
# RETURN --> LONG/LAT TUPLE

def getCoordinates(address):
    #mapQuestDict = json.load( getGeocoding(request, address) )
    #response = requests.get( getGeocoding(request, address) )
    #response = getGeocoding(request, address)
    response = geocoding(address)
    #mapQuestDict = json.loads(response)
    #mapQuestDict = json.loads( response.json() )
    data = response["results"][0]["locations"][0]["latLng"]

    latitude = data["lat"]
    longitude = data["lng"]

    print(latitude, " ", longitude)

    return( (float(latitude), float(longitude)) )

    

    return -1


# Get min and max of population given descriptor

# GIVEN --> POPULATION OPTION (SMALL/MED/LARGE/ETC.)
# RETURN --> POPULATION MIN/MAX TUPLE

# UTLIZES NCES CLASSIFICATIONS
# FORMAT: (>= Lower Bound, < Upper Bound)

def getPopulationScale(populationDescriptor):
    
    match populationDescriptor:
        
        case "town":
            return( (0, 50_000) )
        
        case "small":
            return( (50_000, 100_000) )
        
        case "medium":
            return( (100_000, 250_000) )
        
        case "large":
            return( (250_000, float("inf")) )
        
        case "any":
            return( (0, float("inf")) )

    return (-1, -1)

def populationInRange(population, range):
    if( int(population) >= range[0] and int(population) < range[1] ):
        return True

    return False



# TODO: Should scale radius to workable size, potentially adding the average radius of a city
    # (long/lat gives center of the city, radius around the city would have to add city radius as well) 

# GIVEN --> RADIUS VALUE (MILES)
# RETURN --> MAPQUEST RADIUS SCALE

def getRadius(radiusValue):
    return int(radiusValue) / 1000


# TODO: Should get cities within the radius that fits the population criteria

# GIVEN --> LONG/LAT TUPLE, MIN/MAX POPULATION TUPLE, RADIUS
# RETURN --> LIST OF CITIES

def getCitiesOfPopulationInRange(coordinates, populationRange, radius,
CITY_DICT=json.load( open("./datasets/us_city_info.json") ) ):
    #cityDictionaryAll = csv.DictReader( open("us_cities.csv") )
    #cityDictionaryAll = csv.DictReader( open("./recommendations/us_cities.csv") )
    iLong = coordinates[1]
    iLat = coordinates[0]

    cityDictionaryFinal = []

    #for city in cityDictionaryAll:
    for city in CITY_DICT:
        longDif = abs( float(city["lng"]) - iLong )
        latDif = abs( float(city["lat"]) - iLat )

        if(longDif <= radius and latDif <= radius):
            distance = sqrt( longDif**2 + latDif**2 )
            
            if( distance <= radius and populationInRange(city["population"], populationRange) ):
                cityDictionaryFinal.append(city)

    return cityDictionaryFinal



# Get Score of city, calling another app (somehow)

# GIVEN --> CITY NAME AND STATE NAME
# RETURN --> CALUCLATED CRIME SCORE

def getCrimeScore(city, state):

    crimeScore = safe_living_score.views.get_score_dict(city, state)["safe-living-score"] 


    #url = ("https://localhost:8000/safelivingscore/api/", city, "/", state, "/")192.168.2.68
    #url = ("http://192.168.137.1:8000/safelivingscore/api/", city, "/", state, "/")
    #crimeScore = json.loads( requests.get(url) )

    if(crimeScore == "There was a problem getting a score. No cities in range."):
        return -1

    return float(crimeScore)

