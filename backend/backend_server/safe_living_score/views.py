from typing import OrderedDict
from django.shortcuts import render
import requests
from django.http import JsonResponse
import json
import requests_cache
requests_cache.install_cache()


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

relevant_crimes = {
    'all': {
        "violent-crime", "homicide", "rape-legacy", "rape", "robbery", "aggravated-assault", "property-crime", "burglary", "larceny", "motor-vehicle-theft", "arson"
    },
    'violent_crime': {
        "violent-crime", "aggravated-assault", "homicide", "rape-legacy", "rape", "arson"
    },
    'nonviolent_crime': {
        "robbery", "property-crime", "burglary", "larceny", "motor-vehicle-theft"
    },
    'theft': {
        "robbery", "property-crime", "burglary", "larceny", "motor-vehicle-theft"
    }
}

relevant_crimes_nat = {
    'all': {
        "violent_crime", "homicide", "rape_legacy", "rape_revised", "robbery", "aggravated_assault", "property_crime", "burglary", "larceny", "motor_vehicle_theft", "arson"
    },
    'violent_crime': {
        "violent_crime", "aggravated_assault", "homicide", "rape_legacy", "rape_revised", "arson"
    },
    'nonviolent_crime': {
        "robbery", "property_crime", "burglary", "larceny", "motor_vehicle_theft"
    },
    'theft': {
        "robbery", "property_crime", "burglary", "larceny", "motor-vehicle_theft"
    }
}

def getScore(request, city, state, crime_type = "all"):
    geocoding_key = 'c7qYTGBjRaRkGF7ucqOvpNy6L1Q857oD'
    geocoding_url = f'http://www.mapquestapi.com/geocoding/v1/address?key={geocoding_key}&location={city}, {state}'
    geocoding_data = requests.get(geocoding_url).json()
    lon = geocoding_data['results'][0]['locations'][0]['latLng']['lng']
    lat = geocoding_data['results'][0]['locations'][0]['latLng']['lat']


    lon = float(lon)
    lat = float(lat)
    radius = 100.0
    d = FBI_wrapper()
    result = d.getAgenciesByCoordinates(lat, lon, radius)

    if(not result):
        result = d.getNearestByType(lat, lon, "City")
    
    score_distance_tuple = {}

    #print(f'{result}\n')

    scores = []

    city_name = city

    for k in result:
        if(city in k['agency_name'] and 'City' in k['agency_type_name']):
            res = getScorebyORI2(k['ori'], crime_type, k['agency_name'], k['state_abbr'])
            #print(f'{k["ori"]} : {res}\n')
            if("agency is not a city" not in res):
                right_index = k["agency_name"].find(" Police")
                #city_name = k["agency_name"][0:right_index]
                scores.append(int(res['num-crimes']))
                print(f'number of crimes for {k["agency_name"]}: {res["num-crimes"]}')
        
    

    #print("Score distance tuple: ", score_distance_tuple)
    if(not scores):
        context = {
            "safe-living-score": "There was a problem getting a score. No cities in range."
        }
        return JsonResponse(context)
    
    crime_score = 0
    for p in scores:
        crime_score += p
    
    #Population stuff!
    
    f = open('./safe_living_score/population_data.json')
    population_data = json.load(f)

    

    for d in {" city", " City", " village", " Village"}:
        if(d in city_name):
            city_name = city_name[0:city_name.find(d)]
    
    population = -1

    for k in population_data:
        if(k[2] == stateCodes[state]):
            if(f'{city_name} city' in k[0] or f'{city_name} village' in k[0]):
                population = int(k[1])
    
    if population == -1:
        context = {
            "safe-living-score": "There was a problem getting the safe living score for this location. Population not found."
        }
    else:
        nat_pop = 329484123

        f = open('./safe_living_score/national_data.json')
        national_data = json.load(f)

        national_crimes_list = {}
        national_crimes_list = national_data["results"][0]

        nat_crimes = 0

        for k in relevant_crimes_nat[crime_type]:
            if k in national_crimes_list and national_crimes_list[k]:
                nat_crimes += national_crimes_list[k]
        
        crime_score /= population
        crime_score /= (nat_crimes / nat_pop)

        crime_score = 100.0 - (crime_score - 0.5) * 20.0
        context = {
            "safe-living-score": crime_score
        }
    return JsonResponse(context)

def getScorebyORI2(ORI, crime_type, city_name, state):
    key = 'nHym62MTPDELS0XgtAZLLw0fL3jNWoNvsY2kn315'

    fromDate = 2020
    toDate = 2020
    url = f'https://api.usa.gov/crime/fbi/sapi//api/summarized/agencies/{ORI}/offenses/{fromDate}/{toDate}?api_key={key}'
    ori_crime_data = requests.get(url).json()

    crime_list = {}
    for k in ori_crime_data["results"]:
        crime_list[k["offense"]] = k["actual"]
    
    print(city_name)
    #print(ori_crime_data)

    
    num_crimes = 0

    for k in relevant_crimes[crime_type]:
        if(k in crime_list):
            num_crimes += int(crime_list[k])
    
    context = {
        'num-crimes': num_crimes
    }

    return context


# def getScorebyORI(request, ORI, crime_type):
#     key = 'nHym62MTPDELS0XgtAZLLw0fL3jNWoNvsY2kn315'
#     #censuskey = '7c17ec871d6ede3e816aa8f92d3f7824215e2fa9'
#     agency = ORI
#     fromDate = 2020
#     toDate = 2020
#     url = f'https://api.usa.gov/crime/fbi/sapi//api/summarized/agencies/{agency}/offenses/{fromDate}/{toDate}?api_key={key}'
#     oriCrimeData = requests.get(url).json()
#     url = f'https://api.usa.gov/crime/fbi/sapi//api/agencies/{agency}?api_key={key}'
#     oriData = requests.get(url).json()
#     if(oriData["agency_type_name"] == "City"):
#         state = oriData["state_abbr"]
#         right_index = oriData["agency_name"].find(" Police")
#         cityName = oriData["agency_name"][0:right_index]
#         print(cityName)
#         url = f'https://api.usa.gov/crime/fbi/sapi//api/summarized/estimates/states/{state}/{fromDate}/{toDate}?api_key={key}'
#         summarizedStateData = requests.get(url).json()
        
#         f = open('./safe_living_score/population_data.json')
#         population_data = json.load(f)

#         f = open('./safe_living_score/national_data.json')
#         national_data = json.load(f)

#         population = -1

#         #print(cityName)

#         for d in {" city", " City", " village", " Village"}:
#             if(d in cityName):
#                 cityName = cityName[0:cityName.find(d)]

#         # print(cityName)

#         for k in population_data:
#             if(k[2] == stateCodes[state]):
#                 if(f'{cityName} city' in k[0] or f'{cityName} village' in k[0]):
#                     population = k[1]
#         # for k in state_population_data:
#         #     if(k[2] == stateCodes[state]):
#         #         nationalPopulation = k[1]
#         nationalPopulation = 329484123
        
#         if(population != -1):
            
#             crimeList = {}
#             for k in oriCrimeData["results"]:
#                 crimeList[k["offense"]] = k["actual"]

#             nationalCrimeList = {}
#             nationalCrimeList = national_data["results"][0]

#             crimeList["rape_revised"] = crimeList["rape"]

#             crimeList["rape_legacy"] = crimeList["rape-legacy"]
#             crimeList["property_crime"] = crimeList["property-crime"]
#             crimeList["aggravated_assault"] = crimeList["aggravated-assault"]
#             crimeList["motor_vehicle_theft"] = crimeList["motor-vehicle-theft"]
#             crimeList["violent_crime"] = crimeList["violent-crime"]


#             numCrimes = 0
#             nationalNumCrimes = 0

#             relevant_crimes = {}

#             #print(crime_type)

#             match crime_type:
#                 case ("violent_crime"):
#                     #print("Violent crime POG")
#                     relevant_crimes = {"violent_crime", "aggravated_assault", "homicide", "rape_legacy", "rape_revised", "arson"}
#                 case ("nonviolent_crime"):
#                     #print("NONVIOLENT_CRIME POG")
#                     relevant_crimes = {"robbery", "property_crime", "burglary", "larceny", "motor_vehicle_theft"}
#                 case ("theft"):
#                     #print("Theft POG")
#                     relevant_crimes = {"robbery", "property_crime", "burglary", "larceny", "motor_vehicle_theft"}
#                 case _:
#                     #print("Default POG")
#                     relevant_crimes = {"violent_crime", "homicide", "rape_legacy", "rape_revised", "robbery", "aggravated_assault", "property_crime", "burglary", "larceny", "motor_vehicle_theft", "arson"}

                    

#             for k in relevant_crimes:
#                 if(k in crimeList and k in nationalCrimeList):
#                     if(crimeList[k] is not None and nationalCrimeList[k] is not None):
#                         numCrimes += int(crimeList[k])
#                         nationalNumCrimes += int(nationalCrimeList[k])
                

#             crimeRatio = (int(numCrimes) / int(population))/(int(nationalNumCrimes) / int(nationalPopulation))
#             crime_score = 100.0 - (crimeRatio - 0.5) * 20.0

#             print(f'For {cityName}: Number of crimes: {numCrimes}. Population: {population}. nationalNumCrimes: {nationalNumCrimes}. National Population: {nationalPopulation}')

#             context = {
#                 'city name': cityName,
#                 'state': state,
#                 'population': population,
#                 'state code': stateCodes[state],
#                 'national population': nationalPopulation,
#                 'crime-ratio': crime_score,
#                 'num-crimes': numCrimes
#             }
#             return context
#         else:
#             print("Agency did not pass the population check.")
#             context = {
#                 'agency is not a city': 'true',
#                 'crime-ratio': 0,
#                 'numCrimes': 0
#             }
#             return context
#     else:
#         print("Agency did not pass the ORI type check")
#         context = {
#             'agency is not a city': 'true',
#             'crime-ratio': 0,
#             'numCrimes': 0
#         }
#         return context

# def getCrimeScore(scoreDistanceTupleList):
    
#     sumWeights = 0
#     locationScore = 0
    
#     for scoreDistanceTuple in scoreDistanceTupleList:
        
#         weight = 1 / scoreDistanceTupleList[scoreDistanceTuple]['distance']
#         score = scoreDistanceTupleList[scoreDistanceTuple]['score']
        
#         sumWeights += weight
#         locationScore += score * weight
    
#     if(sumWeights == 0):
#         return "There was a problem loading the crime score. No cities found in area."
    
#     locationScore /= sumWeights
    
#     return locationScore
