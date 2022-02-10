import requests
import json
import os

from django.http import JsonResponse
#import safe_living_score

# import importlib.util
# spec = importlib.util.spec_from_file_location("safe_living_app", "C:/Users/Ryan/Documents/GitHub/team6-safelivingapp/backend/backend_server/safe_living_score")

# sls = importlib.util.module_from_spec(spec)
# spec.loader.exec_module(sls)

CRIME_DATA_EXPLORER_KEY = 'nHym62MTPDELS0XgtAZLLw0fL3jNWoNvsY2kn315'
GEOCODING_KEY = 'c7qYTGBjRaRkGF7ucqOvpNy6L1Q857oD'

# Utility function to download the newest crime data from the FBI Crime Data Explorer
def download_newest_crime_data(request = ""):
    from_date = 2020
    to_date = 2020

    try:
        f = open("./datasets/crime_data.json")
    except FileNotFoundError:
        CRIME_DATA = {}
    else:
        CRIME_DATA = json.load(f)
    
    f = open("./datasets/agencies.json")
    AGENCY_DATA = json.load(f)
    count = 0
    try:
        for state_abbr in AGENCY_DATA:
            print(state_abbr)
            for agency in AGENCY_DATA[state_abbr]:
                if AGENCY_DATA[state_abbr][agency]["ori"] not in CRIME_DATA and AGENCY_DATA[state_abbr][agency]["agency_type_name"] == "City":
                    get_url = f'https://api.usa.gov/crime/fbi/sapi//api/summarized/agencies/{AGENCY_DATA[state_abbr][agency]["ori"]}/offenses/{from_date}/{to_date}?api_key={CRIME_DATA_EXPLORER_KEY}'
                    CRIME_DATA[AGENCY_DATA[state_abbr][agency]["ori"]] = requests.get(get_url).json()
                if AGENCY_DATA[state_abbr][agency]["agency_type_name"] == "City":
                    count += 1
                    if count % 10 == 0:
                        print(f"{count} / 11877. {count/11877 * 100:.2f}%")
        with open("./datasets/crime_data.json", "w") as outfile:
            json.dump(CRIME_DATA, outfile)
        print("Successfully downloaded dataset!")
    except KeyboardInterrupt:
        with open("./datasets/crime_data.json", "w") as outfile:
            json.dump(CRIME_DATA, outfile)
        print("Saved what could be saved")

# Utility function to sort the downloaded crime dataset by state for (hopefully) faster read times.
def sort_crime_data_by_state(request):
    try:
        f = open("./datasets/crime_data.json")
    except FileNotFoundError:
        print("Crime dataset not found. Please download that first.")
    else:
        CRIME_DATA = json.load(f)
    
    SORTED_CRIME_DATA = {}
    
    for agency in CRIME_DATA:
        if agency[0:2] == "NE":
            print("NEBRASKA")

        if not agency[0:2] in SORTED_CRIME_DATA:
            SORTED_CRIME_DATA[agency[0:2]] = {agency: CRIME_DATA[agency]}
        else:
            SORTED_CRIME_DATA[agency[0:2]][agency] = CRIME_DATA[agency]
    
    with open("./datasets/crime_data_sorted.json", "w") as outfile:
        json.dump(SORTED_CRIME_DATA, outfile)
    print("Successfully sorted crime dataset")

def make_city_state_to_ori_dataset():
    AGENCY_DATA = json.load(open('./backend/backend_server/datasets/agencies.json'))
    POPULATION_DATA = json.load(open('./backend/backend_server/datasets/population_data_fixed.json'))

    CITY_STATE_ORI_DATA = {}

    for state in POPULATION_DATA:
        print(state)
        CITY_STATE_ORI_DATA[state] = {}
        for city in POPULATION_DATA[state]:
            CITY_STATE_ORI_DATA[state][city] = []
            for agency in AGENCY_DATA[state]:
                if city in AGENCY_DATA[state][agency]['agency_name'] and "City" in AGENCY_DATA[state][agency]['agency_type_name']:
                    CITY_STATE_ORI_DATA[state][city].append(AGENCY_DATA[state][agency]["ori"])

    with open("./backend/backend_server/datasets/city_ori.json", "w") as outfile:
        json.dump(CITY_STATE_ORI_DATA, outfile)
    print("DONE!")

# Utility function to save crime scores to a dataset
def refresh_crime_scores(request):
    
    try:
        SCORE_DATA = json.load(open("./datasets/score.json"))
    except FileNotFoundError:
        print("Could not find the scores dataset")
        SCORE_DATA = {}
    
    try:
        POPULATION_DATA = json.load(open("./datasets/population_data_fixed.json"))
    except FileNotFoundError:
        print("Could not find the population dataset")
        POPULATION_DATA = {}
    
    try:
        NAT_CRIME_DATA = json.load(open("./datasets/national_data.json"))
    except FileNotFoundError:
        print("Could not find the national crime dataset")
        NAT_CRIME_DATA = {}
    
    try:
        CRIME_DATA = json.load(open("./datasets/crime_data_sorted.json"))
    except FileNotFoundError:
        print("Could not find the crime dataset")
        CRIME_DATA = {}
    
    try:
        AGENCY_DATA = json.load(open("./datasets/agencies.json"))
    except FileNotFoundError:
        print("Could not find the crime dataset")
        AGENCY_DATA = {}
    
    count = 0

    try:
        for state in POPULATION_DATA:
            print(state)
            for town in POPULATION_DATA[state]:
                if int(POPULATION_DATA[state][town]["Population"]) > 500 and town not in SCORE_DATA:
                    #print(f"Calculating scores for {town}, {state}")
                    scores = safe_living_score.views.get_safe_living_score(town, state, POPULATION_DATA, CRIME_DATA, AGENCY_DATA)
                    SCORE_DATA[town] = {
                        "scores": scores,
                        "town-name": town,
                        "state-code": state,
                        "town-type": POPULATION_DATA[state][town]["Type"]
                    }
                count += 1
                if(count % 10 == 0):
                    print(f'{count}')
    except KeyboardInterrupt:
        with open("./datasets/scores.json", "w") as outfile:
            json.dump(SCORE_DATA, outfile)
        print("Saved what could be saved")
    
    with open("./datasets/scores.json", "w") as outfile:
        json.dump(SCORE_DATA, outfile)
    print("Successfully compiled scores dataset")

def fix_population_dataset(request = ""):
    POPULATION_DATA = json.load(open('./datasets/population_data.json'))
    NEW_POPULATION_DATA = {}
    for city in POPULATION_DATA:
        if "NAME" in city[0]:
            continue
        city_name = city[0][0:city[0].index(',')]
        for x in [" city", " village", " CDP"]:
            if x in city_name:
                city_name = city_name[0:city_name.index(f"{x}")]
                city_type = x
        state_abbr = safe_living_score.views.codestoState[city[2]]
        if state_abbr not in NEW_POPULATION_DATA:
            NEW_POPULATION_DATA[state_abbr] = {}
        NEW_POPULATION_DATA[state_abbr][city_name] = {
            "Population": int(city[1]),
            "Type": city_type
        }
    with open("./datasets/population_data_fixed.json", "w") as outfile:
        json.dump(NEW_POPULATION_DATA, outfile)
    print("Successfully compiled population dataset!")
    return JsonResponse({"complete": True})

def  main():
    print(os.getcwd())
    make_city_state_to_ori_dataset()

if __name__ == "__main__":
    main()
