import requests
import json
import os

from django.http import JsonResponse
import safe_living_score

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
def sort_crime_data_by_state(request = ""):
    try:
        f = open("./backend/backend_server/datasets/crime_data.json")
    except FileNotFoundError:
        print("Crime dataset not found. Please download that first.")
    else:
        CRIME_DATA = json.load(f)
    
    SORTED_CRIME_DATA = {}
    
    for agency in CRIME_DATA:
        if not agency[0:2] in SORTED_CRIME_DATA:
            SORTED_CRIME_DATA[agency[0:2]] = {agency: CRIME_DATA[agency]}
        else:
            SORTED_CRIME_DATA[agency[0:2]][agency] = CRIME_DATA[agency]
    
    with open("./datasets/crime_data_sorted.json", "w") as outfile:
        json.dump(SORTED_CRIME_DATA, outfile)
    print("Successfully sorted crime dataset")

# Utility function to save crime scores to a dataset
def refresh_crime_scores(request = ""):
    try:
        f = open("./datasets/geocodes.json")
    except FileNotFoundError:
        print("Could not find the population dataset")
        GEOCODES_DATA = {}
    else:
        GEOCODES_DATA = json.load(f)
    
    try:
        f = open("./datasets/scores.json")
    except FileNotFoundError:
        print("Could not find the scores dataset")
        SCORE_DATA = {}
    else:
        SCORE_DATA = json.load(f)
    
    try:
        for town in GEOCODES_DATA:
            if "city" in town["F"] and town["F"] not in SCORE_DATA:
                print(f"Calculating scores for {town['F']}")
                scores = safe_living_score.views.get_score("", town["F"][0:town["F"].index("city")], safe_living_score.views.codestoState[town["A"]], "all")
                SCORE_DATA[town["F"]] = {
                    "scores": scores,
                    "state-code": safe_living_score.views.codestoState[town["A"]]
                }
    except KeyboardInterrupt:
        with open("./datasets/scores.json", "w") as outfile:
            json.dump(SCORE_DATA, outfile)
        print("Saved what could be saved")
    
    with open("./datasets/scores.json", "w") as outfile:
        json.dump(SCORE_DATA, outfile)
    print("Successfully compiled scores dataset")

# def  main():
#     print(os.getcwd())
#     refresh_crime_scores()

# if __name__ == "__main__":
#     main()
