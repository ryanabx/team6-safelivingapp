from django.shortcuts import render



# PROTOTYPE REQUIREMENTS:

# GIVEN --> CITY, RADIUS, POPULATION SCALE
# RETURN --> CITY WITH HIGHEST SAFETY SCORE

def recommendCity(initialCity, radiusValue, populationPreference):

    startingCoordinates = getCoordinates(initialCity)
    populationScale = getPopulationScale(populationPreference)
    radius = getRadius(radiusValue)

    cities = getCitiesOfPopulationInRange(startingCoordinates, populationScale, radius)

    maxCrimeScore = -1
    recommendedCity = None

    for city in cities: # Basic min/max calculation, but works (for now)
        curScore = getCrimeScore(city)
        
        if curScore > maxCrimeScore:
            maxCrimeScore = curScore 
            recommendedCity = city
    
    return recommendedCity




# TODO: Should get long+lat of city, calling API

# GIVEN --> CITY NAME
# RETURN --> LONG/LAT TUPLE

def getCoordinates(city):
    return -1


# TODO: Should get min and max of population given descriptor

# GIVEN --> POPULATION OPTION (SMALL/MED/LARGE/ETC.)
# RETURN --> POPULATION MIN/MAX TUPLE



def getPopulationScale(populationDescriptor):
    return -1



# TODO: Should scale radius to workable size, potentially adding the average radius of a city
    # (long/lat gives center of the city, radius around the city would have to add city radius as well) 

# GIVEN --> RADIUS VALUE (MILES)
# RETURN --> MAPQUEST RADIUS SCALE

def getRadius(radiusValue):
    return -1


# TODO: Should get cities within the radius that fits the population criteria

# GIVEN --> LONG/LAT TUPLE, MIN/MAX POPULATION TUPLE, RADIUS
# RETURN --> LIST OF CITIES

def getCitiesOfPopulationInRange(coordinates, populationRange, radius):
    return -1



# TODO: Should get Score of city, calling another app (somehow)

# GIVEN --> CITY NAME
# RETURN --> CALUCLATED CRIME SCORE

def getCrimeScore(cityName):
    return -1


# Create your views here.
