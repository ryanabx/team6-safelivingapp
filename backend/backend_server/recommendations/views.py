from math import sqrt
from django.shortcuts import render
import safe_living_score.views
from loc_to_addr.views import geocoding
from django.http import JsonResponse

import json
import requests
import math
import geopy.distance

#TEST WITH: http://localhost:8000/recommendations/api/tulsa/4000/large



# PROTOTYPE REQUIREMENTS:

# GIVEN --> CITY, STATE, RADIUS, POPULATION SCALE
# RETURN --> CITY WITH HIGHEST SAFETY SCORE

def recommendCity(request, initialAddress="", stateID="any", radiusValue=-1, minPopulation=-1, maxPopulation=float("inf"), scoreCategory="safe-living"):
    return JsonResponse(  recommend(initialAddress, radiusValue, stateID, ( float(minPopulation), float(maxPopulation) ), scoreCategory)  )

def recommend(initialAddress="", radiusValue=-1, stateID="any", populationPreference=( -1, float("inf") ), scoreCategory="safe-living"):

    if(initialAddress != ""):
        startingCoordinates = getCoordinates(initialAddress)
        radius = getRadius(radiusValue)
        cities = getCitiesOfPopulationInRange(startingCoordinates, populationPreference, radius)
    
    elif(stateID != "any"):
        cities = getCitiesOfPopulationInState(stateID, populationPreference)

    if(cities != None):
        cityScorePairs = []

        for city in cities:
            cityScore = getScore(city["city"], city["state_id"], scoreCategory)
            cityScorePairs.append( (city, cityScore) )
        
        return {
            "cityPairs" : sorted(cityScorePairs, key=getKey, reverse=True)[0:10]
        }

# Get Key of CityScorePairs
def getKey(item):
    return item[1]




# Get long+lat of city, calling API

# GIVEN --> CITY NAME AND STATE NAME
# RETURN --> LONG/LAT TUPLE

def getCoordinates(address):
    response = geocoding(address)
    data = response["results"][0]["locations"][0]["latLng"]

    latitude = data["lat"]
    longitude = data["lng"]

    print(latitude, " ", longitude)

    return( (float(latitude), float(longitude)) )
    #return -1

def populationInRange(population, range):
    if( int(population) >= range[0] and int(population) < range[1] ):
        return True

    return False



# Scale radius to workable size, potentially adding the average radius of a city
    # (long/lat gives center of the city, radius around the city would have to add city radius as well) 

# GIVEN --> RADIUS VALUE (MILES)
# RETURN --> MAPQUEST RADIUS SCALE

def getRadius(radiusValue):
    return int(radiusValue) #/ 1000




# Gets cities within the radius that fits the population criteria

# GIVEN --> LONG/LAT TUPLE, MIN/MAX POPULATION TUPLE, RADIUS
# RETURN --> LIST OF CITIES

def getCitiesOfPopulationInRange(coordinates, populationRange, radius,
CITY_DICT=json.load( open("./datasets/us_city_info.json") ) ):
    iLong = coordinates[1]
    iLat = coordinates[0]

    cityDictionaryFinal = []

    #for city in cityDictionaryAll:
    for city in CITY_DICT:
        
        distance = geopy.distance.great_circle( (iLat, iLong), ( float(city["lat"]), float(city["lng"]) ) ).miles

        if(distance <= radius):
            if(populationInRange(city["population"], populationRange)):
                cityDictionaryFinal.append(city)

    return cityDictionaryFinal



# Gets cities within a given state that fits the population criteria

def getCitiesOfPopulationInState(stateID, populationRange,
CITY_DICT=json.load( open("./datasets/us_city_info.json") ) ):

    cityDictionaryFinal = []
    
    for city in CITY_DICT:
        if(city["state_id"] == stateID):
            if(populationInRange(city["population"], populationRange)):
                cityDictionaryFinal.append(city)

    return cityDictionaryFinal

# Get Score of city, calling another app
# GIVEN --> CITY NAME AND STATE NAME
# RETURN --> CALUCLATED CRIME SCORE

def getScore(city, state, scoreCategory,
    ORI_DICT = json.load( open("./datasets/city_ori.json") ) ):

    if state in ORI_DICT and city in ORI_DICT[state]:
        if( ORI_DICT[state][city] == [] ):
            return -1

    score_dict = safe_living_score.views.get_safe_living_score(city, state)

    if(scoreCategory == "safe-living"):
        crimeScore = score_dict["safe-living-score"] 
    if(scoreCategory == "property"):
        crimeScore = 100 - score_dict["property_crime"] 
    if(scoreCategory == "violent"):
        crimeScore = 100 - score_dict["violent_crime"] 
    if(scoreCategory == "projected-safe-living"):
        crimeScore = score_dict["projected_score"] 


    #url = ("https://localhost:8000/safelivingscore/api/", city, "/", state, "/")192.168.2.68
    #url = ("http://192.168.137.1:8000/safelivingscore/api/", city, "/", state, "/")
    #crimeScore = json.loads( requests.get(url) )

    #print("message: ", score_dict["error_message"])
    
    if score_dict["error_code"] > 0:
        return -1

    return float(crimeScore)

# def tempGetSpecificCompareRank(city, stateID, crimeCategory,
# CITY_ORI = json.load(open('./datasets/city_ori.json')),
# POPULATION_DATA = json.load(open('./datasets/population_data_fixed.json')),
# CRIME_DATA = json.load(open('./datasets/crime_data_sorted.json'))):
    
#     categoryCount = -1

#     if stateID in CITY_ORI:
#         if city in CITY_ORI[stateID]:
#             if CITY_ORI[stateID][city]:
#                 for agency in CITY_ORI[stateID][city]:
#                     crime_count = safe_living_score.views.get_crime_count(agency, stateID, CRIME_DATA)
#                     categoryCount = int(crime_count[crimeCategory])
    
    
                    
    
    
    return -1



# DEPRECIATED
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

