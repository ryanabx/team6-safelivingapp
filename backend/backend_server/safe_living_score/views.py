from asyncio.windows_events import NULL
from typing import OrderedDict
from django.shortcuts import render
import requests
from django.http import JsonResponse
import json
import requests_cache
requests_cache.install_cache(expire_after=-1) #NOTE Currently cache does not expire. 

from safe_living_score.ori_utils import FBI_wrapper

GEOCODING_KEY = 'c7qYTGBjRaRkGF7ucqOvpNy6L1Q857oD'
NATIONAL_POPULATION = 329484123

CRIME_TYPES = ["all", "violent_crime", "property_crime"]

codestoState = {
    "02": "AK",
    "01": "AL",
    "05": "AR",
    "60": "AS",
    "04": "AZ",
    "06": "CA",
    "08": "CO",
    "09": "CT",
    "11": "DC",
    "10": "DE",
    "12": "FL",
    "13": "GA",
    "66": "GU",
    "15": "HI",
    "19": "IA",
    "16": "ID",
    "17": "IL",
    "18": "IN",
    "20": "KS",
    "21": "KY",
    "22": "LA",
    "25": "MA",
    "24": "MD",
    "23": "ME",
    "26": "MI",
    "27": "MN",
    "29": "MO",
    "28": "MS",
    "30": "MT",
    "37": "NC",
    "38": "ND",
    "31": "NE",
    "33": "NH",
    "34": "NJ",
    "35": "NM",
    "32": "NV",
    "36": "NY",
    "39": "OH",
    "40": "OK",
    "41": "OR",
    "42": "PA",
    "72": "PR",
    "44": "RI",
    "45": "SC",
    "46": "SD",
    "47": "TN",
    "48": "TX",
    "49": "UT",
    "51": "VA",
    "78": "VI",
    "50": "VT",
    "53": "WA",
    "55": "WI",
    "54": "WV",
    "56": "WY"
}

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
    'property_crime': {
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
    'property_crime': {
        "robbery", "property_crime", "burglary", "larceny", "motor_vehicle_theft"
    },
    'theft': {
        "robbery", "property_crime", "burglary", "larceny", "motor-vehicle_theft"
    }
}

#Score types: safe_living_score, violent_crime_score, property_crime_score, crime_score

# Function to retrieve all of the safe living scores
def get_score(request, city, state):
    score_list = get_safe_living_score(city, state)
    return JsonResponse(score_list)

# Gets the crime score for a given city and state
# City should be the full city name, state should be the abbreviation (Ex: Tulsa, OK)
def get_crime_score(city, state, POPULATION_DATA = json.load(open('./datasets/population_data.json')), NATIONAL_CRIME_DATA = json.load(open('./datasets/national_data.json'))["results"][0], CRIME_DATA = json.load(open('./datasets/crime_data_sorted.json'))):
    geocoding_url = f'http://www.mapquestapi.com/geocoding/v1/address?key={GEOCODING_KEY}&location={city}, {state}'
    geocoding_data = requests.get(geocoding_url).json()

    lon = geocoding_data['results'][0]['locations'][0]['latLng']['lng']
    lat = geocoding_data['results'][0]['locations'][0]['latLng']['lat']
    lon = float(lon)
    lat = float(lat)
    tolerance = 100.0
    fbi_wrapper = FBI_wrapper()
    
    agencies_by_coordinates = NULL
    crime_numbers = {"all": [], "violent_crime": [], "property_crime": []}

    while (not crime_numbers["all"]):
        while (not agencies_by_coordinates):
            agencies_by_coordinates = fbi_wrapper.getAgenciesByCoordinates(lat, lon, tolerance)
            tolerance += 10.0
        
        for agency in agencies_by_coordinates:
            if city in agency['agency_name'] and "City" in agency['agency_type_name']:
                agency_crime_score_data = get_crime_count(agency['ori'], agency['state_abbr'], CRIME_DATA)
                if "not_a_city" not in agency_crime_score_data:
                    for crime_type in CRIME_TYPES:
                        crime_numbers[crime_type].append(int(agency_crime_score_data[crime_type]))
                    #print(f'number of crimes for {agency["agency_name"]}: {agency_crime_score_data["num-crimes"]}')
        
        if tolerance > 300.0:
            return {}

    num_crimes = {"all": 0, "violent_crime": 0, "property_crime": 0}
    for type in CRIME_TYPES:
        for x in crime_numbers[type]:
            num_crimes[type] += x

    city_population = 0

    for city_data in POPULATION_DATA:
        if(city_data[2] == stateCodes[state]):
            if(city_data[0].find(f'{city} city') == 0 or city_data[0].find(f'{city} village') == 0):
                city_population = int(city_data[1])
    
    city_name = city

    if city_population == 0:
        for suffix in {" city", " City", " village", " Village"}:
            if(suffix in city_name):
                city_name = city_name[0:city_name.find(suffix)]
        
        for city_data in POPULATION_DATA:
            if city_data[2] == stateCodes[state]:
                for city_data in POPULATION_DATA:
                    if(city_data[2] == stateCodes[state]):
                        if(city_data[0].find(f'{city_name} city') == 0 or city_data[0].find(f'{city_name} village')):
                            city_population = int(city_data[1])

    for city_data in POPULATION_DATA:
        if(city_data[2] == stateCodes[state]):
            if(city_data[0].find(f'{city} CDP') == 0):
                city_population = int(city_data[1])
    
    if city_population == 0:
        for city_data in POPULATION_DATA:
            if city_data[2] == stateCodes[state]:
                for city_data in POPULATION_DATA:
                    if(city_data[2] == stateCodes[state]):
                        if(city_data[0].find(f'{city_name} city') == 0 or city_data[0].find(f'{city_name} village')):
                            city_population = int(city_data[1])

    if city_population == 0:
        return {}
    
    national_crimes = {"all": 0, "violent_crime": 0, "property_crime": 0}

    for crime_type in CRIME_TYPES:
        for city_data in relevant_crimes_nat[crime_type]:
            if city_data in NATIONAL_CRIME_DATA and NATIONAL_CRIME_DATA[city_data]:
                national_crimes[crime_type] += NATIONAL_CRIME_DATA[city_data]
    
    #TODO: Find a good normalization for crime score
    score = {"all": 0, "violent_crime": 0, "property_crime": 0}
    for crime_type in CRIME_TYPES:
        score[crime_type] = (num_crimes[crime_type] / city_population) / (national_crimes[crime_type] / NATIONAL_POPULATION)
    
    print(f'(Number of crimes: {num_crimes["all"]} / City Pop: {city_population}) / (National crimes: {national_crimes["all"]} / National Pop: {NATIONAL_POPULATION})')

    print()
    vcrime1 = 0.02
    vcrime2 = 8.8
    pcrime1 = 0.1
    pcrime2 = 4.75

    acrime1 = (vcrime1 + pcrime1) / 2
    acrime2 = (vcrime2 + pcrime2) / 2

    #Test normalization
    score["violent_crime"] = (score["violent_crime"] - vcrime1) / (vcrime2 - vcrime1) * 100
    score["property_crime"] = (score["property_crime"] - pcrime1) / (pcrime2 - pcrime1) * 100
    score["all"] = (score["violent_crime"] + score["property_crime"]) / 2

    score["violent_crime"] = round(score["violent_crime"])
    score["property_crime"]= round(score["property_crime"])
    score["all"] = round(score["all"])
                
    return score

# Gets the safe living score for a given city and state.
def get_safe_living_score(city, state, POPULATION_DATA = json.load(open('./datasets/population_data.json')), NATIONAL_CRIME_DATA = json.load(open('./datasets/national_data.json'))["results"][0], CRIME_DATA = json.load(open('./datasets/crime_data_sorted.json'))):
    score = get_crime_score(city, state, POPULATION_DATA, NATIONAL_CRIME_DATA, CRIME_DATA)
    score["safe-living-score"] = 100 - score["all"]
    return score

# Gets the safe living score for a given city and state.
# def get_safe_living_score_old(city, state, crime_type = "all"):
#     geocoding_url = f'http://www.mapquestapi.com/geocoding/v1/address?key={GEOCODING_KEY}&location={city}, {state}'
#     geocoding_data = requests.get(geocoding_url).json()
#     lon = geocoding_data['results'][0]['locations'][0]['latLng']['lng']
#     lat = geocoding_data['results'][0]['locations'][0]['latLng']['lat']

#     lon = float(lon)
#     lat = float(lat)
#     radius = 100.0
#     d = FBI_wrapper()
#     result = d.getAgenciesByCoordinates(lat, lon, radius)

#     if(not result):
#         result = d.getNearestByType(lat, lon, "City")
    
#     score_distance_tuple = {}

#     #print(f'{result}\n')

#     scores = []

#     city_name = city

#     for city_data in result:
#         if(city in city_data['agency_name'] and 'City' in city_data['agency_type_name']):
#             res = getScorebyORI2(city_data['ori'], crime_type, city_data['agency_name'], city_data['state_abbr'])
#             #print(f'{city_data["ori"]} : {res}\n')
#             if("agency is not a city" not in res):
#                 right_index = city_data["agency_name"].find(" Police")
#                 #city_name = city_data["agency_name"][0:right_index]
#                 scores.append(int(res['num-crimes']))
#                 print(f'number of crimes for {city_data["agency_name"]}: {res["num-crimes"]}')
        
    

#     #print("Score distance tuple: ", score_distance_tuple)
#     if(not scores):
#         context = {
#             "safe-living-score": "There was a problem getting a score. No cities in range."
#         }
#         return JsonResponse(context)
    
#     crime_score = 0
#     for p in scores:
#         crime_score += p
    
#     #Population stuff!
    
#     f = open('./datasets/population_data.json')
#     population_data = json.load(f)

    

    
    
#     population = -1

#     for city_data in population_data:
#         if(city_data[2] == stateCodes[state]):
#             if(city_data[0].find(f'{city_name} city') == 0 or city_data[0].find(f'{city_name} village') == 0):
#                 population = int(city_data[1])
    
#     if population == -1:
#         for d in {" city", " City", " village", " Village"}:
#             if(d in city_name):
#                 city_name = city_name[0:city_name.find(d)]
        
#         for city_data in population_data:
#             if city_data[2] == stateCodes[state]:
#                 for city_data in population_data:
#                     if(city_data[2] == stateCodes[state]):
#                         if(city_data[0].find(f'{city_name} city') == 0 or city_data[0].find(f'{city_name} village')):
#                             population = int(city_data[1])
    
    
#     if population == -1:
#         context = {
#             "safe-living-score": "There was a problem getting the safe living score for this location. Population not found."
#         }
#     else:
#         nat_pop = 329484123

#         print(f'{city_name}: {population}')

#         f = open('./datasets/national_data.json')
#         national_data = json.load(f)

#         national_crimes_list = {}
#         national_crimes_list = national_data["results"][0]

#         nat_crimes = 0

#         for city_data in relevant_crimes_nat[crime_type]:
#             if city_data in national_crimes_list and national_crimes_list[city_data]:
#                 nat_crimes += national_crimes_list[city_data]
        
#         crime_score /= population
#         crime_score /= (nat_crimes / nat_pop)

#         crime_score = 100.0 - (crime_score - 0.5) * 20.0
#         context = {
#             "safe-living-score": crime_score
#         }
#     return JsonResponse(context)

# Gets the number of crimes for a certain ORI
def get_crime_count(ORI, state_abbr, CRIME_DATA = json.load(open('./datasets/crime_data_sorted.json'))):
    crime_list = {}
    for city_data in CRIME_DATA[state_abbr][ORI]["results"]:
        crime_list[city_data["offense"]] = city_data["actual"]
    num_crimes = {"all": 0, "violent_crime": 0, "property_crime": 0}
    for crime_type in CRIME_TYPES:
        for city_data in relevant_crimes[crime_type]:
            if(city_data in crime_list):
                num_crimes[crime_type] += int(crime_list[city_data])

    return num_crimes


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

#         for city_data in population_data:
#             if(city_data[2] == stateCodes[state]):
#                 if(f'{cityName} city' in city_data[0] or f'{cityName} village' in city_data[0]):
#                     population = city_data[1]
#         # for city_data in state_population_data:
#         #     if(city_data[2] == stateCodes[state]):
#         #         nationalPopulation = city_data[1]
#         nationalPopulation = 329484123
        
#         if(population != -1):
            
#             crimeList = {}
#             for city_data in oriCrimeData["results"]:
#                 crimeList[city_data["offense"]] = city_data["actual"]

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

                    

#             for city_data in relevant_crimes:
#                 if(city_data in crimeList and city_data in nationalCrimeList):
#                     if(crimeList[city_data] is not None and nationalCrimeList[city_data] is not None):
#                         numCrimes += int(crimeList[city_data])
#                         nationalNumCrimes += int(nationalCrimeList[city_data])
                

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
