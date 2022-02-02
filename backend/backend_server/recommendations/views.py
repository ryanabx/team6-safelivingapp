from math import sqrt
from django.shortcuts import render
from safe_living_score.views import getScore
from loc_to_addr.views import getGeocoding

import csv
#csv.DictReader(file)



# PROTOTYPE REQUIREMENTS:

# GIVEN --> CITY, STATE, RADIUS, POPULATION SCALE
# RETURN --> CITY WITH HIGHEST SAFETY SCORE

def recommendCity(request, initialAddress, radiusValue, populationPreference="any"):

    startingCoordinates = getCoordinates(initialAddress)
    populationScale = getPopulationScale(populationPreference)
    radius = getRadius(radiusValue)

    cities = getCitiesOfPopulationInRange(startingCoordinates, populationScale, radius)

    maxCrimeScore = -1
    recommendedCity = None

    for city in cities: # Basic min/max calculation, but works (for now)
        curScore = getCrimeScore(city["city"], city["state"])
        
        if curScore > maxCrimeScore:
            maxCrimeScore = curScore 
            recommendedCity = city
    
    return ("" + recommendedCity["city"] + ", " + recommendedCity["state"])




# Get long+lat of city, calling API

# GIVEN --> CITY NAME AND STATE NAME
# RETURN --> LONG/LAT TUPLE

def getCoordinates(address):
    return getGeocoding(address)


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
            return( (250,000, float("inf")) )
        
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
    return int(radiusValue) * 1000


# TODO: Should get cities within the radius that fits the population criteria

# GIVEN --> LONG/LAT TUPLE, MIN/MAX POPULATION TUPLE, RADIUS
# RETURN --> LIST OF CITIES

def getCitiesOfPopulationInRange(coordinates, populationRange, radius):
    cityDictionaryAll = csv.DictReader( open("us_cities.csv") )
    iLong = coordinates[0]
    iLat = coordinates[1]

    cityDictionaryFinal = []

    for city in cityDictionaryAll:
        longDif = abs(int(city["lng"]) - iLong)
        latDif = abs(int(city["lat"]) - iLat)

        if(longDif <= radius and latDif <= radius):
            distance = sqrt( longDif**2 + latDif**2 )
            
            if( distance <= radius and populationInRange(city["population"], populationRange) ):
                cityDictionaryFinal.append(city)

    return cityDictionaryFinal



# Get Score of city, calling another app (somehow)

# GIVEN --> CITY NAME AND STATE NAME
# RETURN --> CALUCLATED CRIME SCORE

def getCrimeScore(city, state):
    return getScore(city, state)

