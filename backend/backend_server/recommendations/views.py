from math import sqrt
from django.shortcuts import render
import safe_living_score.views
from loc_to_addr.views import geocoding
from django.http import JsonResponse

import csv
import json
import requests
import math
import geopy.distance
#csv.DictReader(file)

#TEST WITH: http://localhost:8000/recommendations/api/tulsa/4000/large



# PROTOTYPE REQUIREMENTS:

# GIVEN --> CITY, STATE, RADIUS, POPULATION SCALE
# RETURN --> CITY WITH HIGHEST SAFETY SCORE

def recommendCity(request, initialAddress="", stateID="any", radiusValue=-1, minPopulation=-1, maxPopulation=float("inf")):
    return JsonResponse( recommend(initialAddress, radiusValue, stateID, ( float(minPopulation), float(maxPopulation) ) ) )


# def recommend(initialAddress, radiusValue, populationPreference=( -1, float("inf") )):

#     startingCoordinates = getCoordinates(initialAddress)
#     #populationScale = getPopulationScale(populationPreference)
#     radius = getRadius(radiusValue)

#     cities = getCitiesOfPopulationInRange(startingCoordinates, populationPreference, radius)

#     maxScore = -1
#     recommendedCity = None

#     for city in cities: # Basic min/max calculation, but works (for now)
#         print(city)
#         curScore = getCrimeScore(city["city"], city["state_id"])
#         print("curScore = ", curScore)
        
#         if curScore >= maxScore:
#             maxScore = curScore 
#             recommendedCity = city
    
#     if(recommendedCity == None):

#         context = {
#             "city" : "No City Found",
#             "error_code": 1,
#             "error_message": "No recommended city found"
#     }
#     else:

#         context = {
#             #"recommendation" : ( "" + recommendedCity["city"] + ", " + recommendedCity["state"] )
#             "city" : recommendedCity["city"],
#             "state" : recommendedCity["state"],
#             "population" : recommendedCity["population"],
#             "error_code": 0,
#             "error_message": "",
#             "Safe Living Score" : maxScore
#         }
    
#     return context



def recommend(initialAddress="", radiusValue=-1, stateID="any", populationPreference=( -1, float("inf") )):

    if(initialAddress != ""):
        startingCoordinates = getCoordinates(initialAddress)
        radius = getRadius(radiusValue)
        cities = getCitiesOfPopulationInRange(startingCoordinates, populationPreference, radius)
    
    elif(stateID != "any"):
        cities = getCitiesOfPopulationInState(stateID, populationPreference)

    if(cities != None):
        cityScorePairs = []

        for city in cities:
            print("score = ", getCrimeScore(city["city"], city["state_id"]))
            cityScore = getCrimeScore(city["city"], city["state_id"])
            cityScorePairs.append( (city, cityScore) )
        
        return {
            "cityPairs" : sorted(cityScorePairs, key=getKey, reverse=True)[0:10]
        }


    # maxScore = -1
    # recommendedCity = None

    # for city in cities: # Basic min/max calculation, but works (for now)
    #     print(city)
    #     curScore = getCrimeScore(city["city"], city["state_id"])
    #     print("curScore = ", curScore)
        
    #     if curScore >= maxScore:
    #         maxScore = curScore 
    #         recommendedCity = city
    
    # if(recommendedCity == None):

    #     context = {
    #         "city" : "No City Found",
    #         "error_code": 1,
    #         "error_message": "No recommended city found"
    # }
    # else:

    #     context = {
    #         #"recommendation" : ( "" + recommendedCity["city"] + ", " + recommendedCity["state"] )
    #         "city" : recommendedCity["city"],
    #         "state" : recommendedCity["state"],
    #         "population" : recommendedCity["population"],
    #         "error_code": 0,
    #         "error_message": "",
    #         "Safe Living Score" : maxScore
    #     }
    
    # return context

def getKey(item):
    return item[1]



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
    #return -1


# Get min and max of population given descriptor

# GIVEN --> POPULATION OPTION (SMALL/MED/LARGE/ETC.)
# RETURN --> POPULATION MIN/MAX TUPLE

# UTLIZES NCES CLASSIFICATIONS
# FORMAT: (>= Lower Bound, < Upper Bound)

#DEPRECIATED

#def getPopulationScale(populationDescriptor):
    
#    match populationDescriptor:
        
#        case "town":
#            return( (0, 50_000) )
        
 #       case "small":
  #          return( (50_000, 100_000) )
        
   #     case "medium":
    #        return( (100_000, 250_000) )
        
     #   case "large":
      #      return( (250_000, float("inf")) )
        
       # case "any":
        #    return( (0, float("inf")) )

    # return (-1, -1)

def populationInRange(population, range):
    if( int(population) >= range[0] and int(population) < range[1] ):
        return True

    return False



# TODO: Should scale radius to workable size, potentially adding the average radius of a city
    # (long/lat gives center of the city, radius around the city would have to add city radius as well) 

# GIVEN --> RADIUS VALUE (MILES)
# RETURN --> MAPQUEST RADIUS SCALE

def getRadius(radiusValue):
    return int(radiusValue) #/ 1000


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
        
        distance = geopy.distance.great_circle( (iLat, iLong), ( float(city["lat"]), float(city["lng"]) ) ).km

        if(distance <= radius):
            if(populationInRange(city["population"], populationRange)):
                cityDictionaryFinal.append(city)

    return cityDictionaryFinal


def getCitiesOfPopulationInState(stateID, populationRange,
CITY_DICT=json.load( open("./datasets/us_city_info.json") ) ):
    #cityDictionaryAll = csv.DictReader( open("us_cities.csv") )
    #cityDictionaryAll = csv.DictReader( open("./recommendations/us_cities.csv") )

    cityDictionaryFinal = []

    #for city in cityDictionaryAll:
    for city in CITY_DICT:
        
        #distance = geopy.distance.great_circle( (iLat, iLong), ( float(city["lat"]), float(city["lng"]) ) ).km

        #if(distance <= radius):
        if(city["state_id"] == stateID):
            if(populationInRange(city["population"], populationRange)):
                cityDictionaryFinal.append(city)

    return cityDictionaryFinal



# def getLongLatDistance(iLong, iLat, curLong, curLat):
    
#     longDifference = abs(iLong - curLong)
#     latDifference = abs(iLat - curLat)
    
#     EARTH_RADIUS = 6371 # Radius in kilometers

#     radLongDifference = (longDifference * math.pi) / 180
#     radLatDifference = (latDifference * math.pi) / 180
#     iRadLat = (iLat * math.pi) / 180
#     curRadLat = (curLat * math.pi) / 180

#     aFormula = ( math.sin(radLatDifference/2) ** 2 ) + ( math.cos(iRadLat) * math.cos(curRadLat) ) + ( math.sin(radLongDifference/2) ** 2 )
#     #bFormula = 2 * math.atan2( math.sqrt(aFormula), math.sqrt(1-aFormula) )
#     bFormula = 2 * math.asin( math.sqrt(aFormula) )
#     finalDistance = EARTH_RADIUS * bFormula

#     return finalDistance



# Get Score of city, calling another app (somehow)

# GIVEN --> CITY NAME AND STATE NAME
# RETURN --> CALUCLATED CRIME SCORE

def getCrimeScore(city, state,
    ORI_DICT = json.load( open("./datasets/city_ori.json") ) ):

    if state in ORI_DICT and city in ORI_DICT[state]:
        if( ORI_DICT[state][city] == [] ):
            return -1

    score_dict = safe_living_score.views.get_score_dict(city, state)

    crimeScore = score_dict["safe-living-score"] 


    #url = ("https://localhost:8000/safelivingscore/api/", city, "/", state, "/")192.168.2.68
    #url = ("http://192.168.137.1:8000/safelivingscore/api/", city, "/", state, "/")
    #crimeScore = json.loads( requests.get(url) )

    #print("message: ", score_dict["error_message"])
    
    if score_dict["error_code"] > 0:
        return -1

    return float(crimeScore)

