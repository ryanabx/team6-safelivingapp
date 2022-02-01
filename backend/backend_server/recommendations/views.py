from django.shortcuts import render
from safe_living_score.views import getScore
from loc_to_addr.views import getGeocoding



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




# Get long+lat of city, calling API

# GIVEN --> CITY NAME AND STATE NAME
# RETURN --> LONG/LAT TUPLE

def getCoordinates(city, state):
    return getGeocoding("" + city + ", " + state)


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
            return( (50_001, 100_000) )
        
        case "medium":
            return( (100_000, 250_000) )
        
        case "large":
            return( (250,000, float("inf")) )

    return (-1, -1)



# TODO: Should scale radius to workable size, potentially adding the average radius of a city
    # (long/lat gives center of the city, radius around the city would have to add city radius as well) 

# GIVEN --> RADIUS VALUE (MILES)
# RETURN --> MAPQUEST RADIUS SCALE

def getRadius(radiusValue):
    return radiusValue


# TODO: Should get cities within the radius that fits the population criteria

# GIVEN --> LONG/LAT TUPLE, MIN/MAX POPULATION TUPLE, RADIUS
# RETURN --> LIST OF CITIES

def getCitiesOfPopulationInRange(coordinates, populationRange, radius):
    return -1



# Get Score of city, calling another app (somehow)

# GIVEN --> CITY NAME AND STATE NAME
# RETURN --> CALUCLATED CRIME SCORE

def getCrimeScore(city, state):
    return getScore(city, state)

