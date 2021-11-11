from typing import OrderedDict
from django.shortcuts import render
import requests
from django.http import JsonResponse
import json

from safe_living_score.ori_utils import FBI_wrapper

stateCodes = {
    "AK": "02",
    "AL": "01",
    "AR": "05",
    "AS": "60",
    "AZ": "04",
    "CA": "06",
    "CO": "08",
    "CT": "09",
    "DC": "11",
    "DE": "10",
    "FL": "12",
    "GA": "13",
    "GU": "66",
    "HI": "15",
    "IA": "19",
    "ID": "16",
    "IL": "17",
    "IN": "18",
    "KS": "20",
    "KY": "21",
    "LA": "22",
    "MA": "25",
    "MD": "24",
    "ME": "23",
    "MI": "26",
    "MN": "27",
    "MO": "29",
    "MS": "28",
    "MT": "30",
    "NC": "37",
    "ND": "38",
    "NE": "31",
    "NH": "33",
    "NJ": "34",
    "NM": "35",
    "NV": "32",
    "NY": "36",
    "OH": "39",
    "OK": "40",
    "OR": "41",
    "PA": "42",
    "PR": "72",
    "RI": "44",
    "SC": "45",
    "SD": "46",
    "TN": "47",
    "TX": "48",
    "UT": "49",
    "VA": "51",
    "VI": "78",
    "VT": "50",
    "WA": "53",
    "WI": "55",
    "WV": "54",
    "WY": "56"
}

def getScore(request, lon, lat, radius):
    lon = float(lon)
    lat = float(lat)
    radius = float(radius)
    d = FBI_wrapper()
    result = d.getAgenciesByCoordinates(lat, lon, radius)

    if(not result):
        result = d.getNearestByType(lat, lon, "City")
    
    score_distance_tuple = {}

    for k in result:
        
        res = getScorebyORI("", k["ori"])
        print("Resulting dict: ", res)
        if("agency is not a city" not in res):
            score_distance_tuple[k["ori"]] = {}
            score_distance_tuple[k["ori"]]["score"] = float(res['crime-ratio'])
            score_distance_tuple[k["ori"]]["distance"] = float(k["distance"])
        

    print("Score distance tuple: ", score_distance_tuple)
    crime_score = getCrimeScore(score_distance_tuple)
    
    context = {
        "safe-living-score": crime_score
    }
    return JsonResponse(context)

def getScorebyORI(request, ORI):
    key = 'nHym62MTPDELS0XgtAZLLw0fL3jNWoNvsY2kn315'
    censuskey = '7c17ec871d6ede3e816aa8f92d3f7824215e2fa9'
    agency = ORI
    fromDate = 2020
    toDate = 2020
    url = f'https://api.usa.gov/crime/fbi/sapi//api/summarized/agencies/{agency}/offenses/{fromDate}/{toDate}?api_key={key}'
    oriCrimeData = requests.get(url).json()
    url = f'https://api.usa.gov/crime/fbi/sapi//api/agencies/{agency}?api_key={key}'
    oriData = requests.get(url).json()
    if(oriData["agency_type_name"] == "City"):
        state = oriData["state_abbr"]
        right_index = oriData["agency_name"].find(" Police")
        cityName = oriData["agency_name"][0:right_index]
        print(cityName)
        url = f'https://api.usa.gov/crime/fbi/sapi//api/summarized/estimates/states/{state}/{fromDate}/{toDate}?api_key={key}'
        summarizedStateData = requests.get(url).json()
        
        f = open('./safe_living_score/population_data.json')
        population_data = json.load(f)

        f = open('./safe_living_score/state_population_data.json')
        state_population_data = json.load(f)

        population = -1

        for k in population_data:
            if(k[2] == stateCodes[state]):
                if(cityName in k[0] and "city" in k[0]):
                    population = k[1]
        for k in state_population_data:
            if(k[2] == stateCodes[state]):
                statePopulation = k[1]
        
        if(population != -1):
            
            crimeList = {}
            for k in oriCrimeData["results"]:
                crimeList[k["offense"]] = k["actual"]

            stateCrimeList = {}
            stateCrimeList = summarizedStateData["results"][0]

            crimeList["rape_revised"] = crimeList["rape"]
            crimeList["rape_legacy"] = crimeList["rape-legacy"]
            crimeList["property_crime"] = crimeList["property-crime"]
            crimeList["aggravated_assault"] = crimeList["aggravated-assault"]
            crimeList["motor_vehicle_theft"] = crimeList["motor-vehicle-theft"]
            crimeList["violent_crime"] = crimeList["violent-crime"]


            numCrimes = 0
            stateNumCrimes = 0

            for k in {"violent_crime", "homicide", "rape_legacy", "rape_revised", "robbery", "aggravated_assault", "property_crime", "burglary", "larceny", "motor_vehicle_theft", "arson"}:
                if(k in crimeList and k in stateCrimeList):
                    if(crimeList[k] is not None and stateCrimeList[k] is not None):
                        numCrimes += int(crimeList[k])
                        stateNumCrimes += int(stateCrimeList[k])
                

            crimeRatio = (int(numCrimes) / int(population))/(int(stateNumCrimes) / int(statePopulation))

            context = {
                'city name': cityName,
                'state': state,
                'population': population,
                'state code': stateCodes[state],
                'state population': statePopulation,
                'crime-ratio': crimeRatio
            }
            return context
        else:
            context = {
                'agency is not a city': 'true',
                'crime-ratio': 0
            }
            return context
    else:
        context = {
            'agency is not a city': 'true',
            'crime-ratio': 0
        }
        return context

def getCrimeScore(scoreDistanceTupleList):
    
    sumWeights = 0
    locationScore = 0
    
    for scoreDistanceTuple in scoreDistanceTupleList:
        
        weight = 1 / scoreDistanceTupleList[scoreDistanceTuple]['distance']
        score = scoreDistanceTupleList[scoreDistanceTuple]['score']
        
        sumWeights += weight
        locationScore += score * weight
    
    
    locationScore /= sumWeights
    
    return locationScore
