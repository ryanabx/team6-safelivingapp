#from asyncio.windows_events import NULL
from typing import OrderedDict
from django.shortcuts import render
import requests
from django.http import JsonResponse
import json
#import requests_cache
#requests_cache.install_cache(expire_after=-1) #NOTE Currently cache does not expire. 

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
        "violent-crime", "property-crime"
    },
    'violent_crime': {
        "violent-crime"
    },
    'property_crime': {
        "property-crime"
    }
}

#Score types: safe_living_score, violent_crime_score, property_crime_score, crime_score

# Function to retrieve all of the safe living scores
def get_score(request, city, state):
    print("HELLO")
    score_list = get_safe_living_score(city, state)
    score_list["city"] = city
    score_list["state"] = state
    return JsonResponse(score_list)

def get_score_dict(city, state):
    score_list = get_safe_living_score(city, state)
    score_list["city"] = city
    score_list["state"] = state
    return score_list


# Gets the crime score for a given city and state
# City should be the full city name, state should be the abbreviation (Ex: Tulsa, OK)
def get_crime_score(city, state,
POPULATION_DATA = json.load(open('./datasets/population_data_fixed.json')),
CRIME_DATA = json.load(open('./datasets/crime_data_sorted.json')),
AGENCIES = json.load(open('./datasets/agencies.json')),
CITY_ORI = json.load(open('./datasets/city_ori.json'))
):
    # geocoding_url = f'http://www.mapquestapi.com/geocoding/v1/address?key={GEOCODING_KEY}&location={city}, {state}'
    # geocoding_data = requests.get(geocoding_url).json()

    # #print(f'Starting crime score calculation for {city}, {state}')

    # lon = geocoding_data['results'][0]['locations'][0]['latLng']['lng']
    # lat = geocoding_data['results'][0]['locations'][0]['latLng']['lat']
    # lon = float(lon)
    # lat = float(lat)
    # fbi_wrapper = FBI_wrapper()
    
    # agencies_by_coordinates = None
    crime_numbers = {"all": [], "violent_crime": [], "property_crime": []}

    if state in CITY_ORI and city in CITY_ORI[state]:
        if CITY_ORI[state][city]:
            for agency in CITY_ORI[state][city]:
                crime_count = get_crime_count(agency, state, CRIME_DATA)
                for crime_type in CRIME_TYPES:
                    crime_numbers[crime_type].append(int(crime_count[crime_type]))
        else:
            return {"all": -1, "violent_crime": -1, "property_crime": -1}
    else:
        return {"all": -1, "violent_crime": -1, "property_crime": -1}

    # agencies_by_coordinates = fbi_wrapper.getAgenciesByCoordinates(lat, lon, 300.0, AGENCIES)
    # if not agencies_by_coordinates:
    #     return {"all": -1, "violent_crime": -1, "property_crime": -1}

    # for agency in agencies_by_coordinates:
    #     if city in agency['agency_name'] and "City" in agency['agency_type_name']:
    #         agency_crime_score_data = get_crime_count(agency['ori'], agency['state_abbr'], CRIME_DATA)
    #         if "not_a_city" not in agency_crime_score_data:
    #             for crime_type in CRIME_TYPES:
    #                 crime_numbers[crime_type].append(int(agency_crime_score_data[crime_type]))
    #             #print(f'{agency["agency_name"]}, {agency["state_abbr"]}, {agency["ori"]}: {agency_crime_score_data["all"]}')
    
    # agencies_by_coordinates = None

    # if not crime_numbers["all"]:
    #     return {"all": -1, "violent_crime": -1, "property_crime": -1}

    num_crimes = {"all": 0, "violent_crime": 0, "property_crime": 0}
    for type in CRIME_TYPES:
        for x in crime_numbers[type]:
            num_crimes[type] += x

    if num_crimes["all"] < 10:
        return {"all": -1, "violent_crime": -1, "property_crime": -1}

    city_population = 0

    if city in POPULATION_DATA[state]:
        city_population = int(POPULATION_DATA[state][city]["Population"])
    else:
        city_name = city
        for suffix in [" city", " City", " village", " Village"]:
            if suffix in city_name: city_name = city_name[0:city_name.find(suffix)]
        if city_name in POPULATION_DATA[state]:
            city_population = int(POPULATION_DATA[state][city_name]["Population"])
        else:
            return {"all": -1, "violent_crime": -1, "property_crime": -1}
    
    if city_population == 0:
        return {"all": -1, "violent_crime": -1, "property_crime": -1}
    
    #print("HI")
    national_crimes = {"all": 7765143, "violent_crime": 1313105, "property_crime": 6452038}

    #print(f'(Number of crimes: {num_crimes["all"]} / City Pop: {city_population}) / (National crimes: {national_crimes["all"]} / National Pop: {NATIONAL_POPULATION})')
    score = {"all": 0, "violent_crime": 0, "property_crime": 0}
    for crime_type in CRIME_TYPES:
        score[crime_type] = (num_crimes[crime_type] / city_population) / (national_crimes[crime_type] / NATIONAL_POPULATION)
    

    vcrime1 = 0.025
    vcrime2 = 8.36
    pcrime1 = 0.18
    pcrime2 = 4.54

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
def get_safe_living_score(city, state,
POPULATION_DATA = json.load(open('./datasets/population_data_fixed.json')),
CRIME_DATA = json.load(open('./datasets/crime_data_sorted.json')),
AGENCIES = json.load(open('./datasets/agencies.json')),
CITY_ORI = json.load(open('./datasets/city_ori.json'))
):
    #print(f'Get safe living score for {city}, {state}')
    score = get_crime_score(city, state, POPULATION_DATA, CRIME_DATA, AGENCIES, CITY_ORI)
    if score["all"] == -1:
        score["safe-living-score"] = -1
    else:
        score["safe-living-score"] = 100 - score["all"]
    return score

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