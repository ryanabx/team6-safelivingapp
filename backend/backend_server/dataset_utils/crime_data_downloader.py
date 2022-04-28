# Utility function to download the newest crime data from the FBI Crime Data Explorer
import json
from django.http import JsonResponse
import requests
import os
import numpy

import safe_living_score

CRIME_DATA_EXPLORER_KEY = json.load(open('./API_KEYS.json'))["crime_data_explorer"]

def make_crime_score_dataset(
    request = "",
    CITY_LIST = json.load(open("./datasets/search_suggestions.json")),
    POPULATION_DATA = json.load(open('./datasets/population_data_fixed.json')),
    CRIME_DATA = json.load(open('./datasets/crime_data_sorted.json')),
    CITY_ORI = json.load(open('./datasets/city_ori.json')), include_reviews = False,
    PROJECTED_DATA = json.load(open('./datasets/ori_future_preds.json')),
    SAVE_PATH = "./datasets/score_error_check.json",
    SAVE_PATH2 = "./datasets/sorted_violent.json",
    SAVE_PATH3 = "./datasets/sorted_property.json",
    SAVE_PATH4 = "./datasets/sorted_all.json",
    SAVE_PATH5 = "./datasets/sorted_violent_projected.json",
    SAVE_PATH6 = "./datasets/sorted_property_projected.json",
    SAVE_PATH7 = "./datasets/sorted_all_projected.json"
):
    ALL_SCORES = {}
    ALL_CRIME = []
    VIOLENT_CRIME = []
    PROPERTY_CRIME = []
    VIOLENT_CRIME_PROJECTED = []
    PROPERTY_CRIME_PROJECTED = []
    ALL_CRIME_PROJECTED = []
    for state in POPULATION_DATA:
        ALL_SCORES[state] = {}
        print(state)
        for city in POPULATION_DATA[state]:
            result = safe_living_score.views.get_safe_living_score_legacy(
                city, state,
                POPULATION_DATA,
                CRIME_DATA,
                CITY_ORI,
                include_reviews,
                PROJECTED_DATA,
                False
            )
            ALL_SCORES[state][city] = result
            if result["error_code"] == 0:
                VIOLENT_CRIME.append((city,state, result["violent_crime"]))
                PROPERTY_CRIME.append((city,state, result["property_crime"]))
                ALL_CRIME.append((city, state, result["all"]))

                if result["projected_all"] != -1:
                    ALL_SCORES[state][city]["projected_violent_crime"] = result["projected_violent_crime"]
                    ALL_SCORES[state][city]["projected_property_crime"] = result["projected_property_crime"]
                    ALL_SCORES[state][city]["projected_all"] = result["projected_all"]
                    VIOLENT_CRIME_PROJECTED.append((city,state, result["projected_violent_crime"]))
                    PROPERTY_CRIME_PROJECTED.append((city,state, result["projected_property_crime"]))
                    ALL_CRIME_PROJECTED.append((city, state, result["projected_all"]))
        
    
    VIOLENT_CRIME_SORTED = sorted(VIOLENT_CRIME, key=lambda x: x[2])
    PROPERTY_CRIME_SORTED = sorted(PROPERTY_CRIME, key=lambda x: x[2])
    ALL_CRIME_SORTED = sorted(ALL_CRIME, key=lambda x: x[2])

    VIOLENT_CRIME_PROJECTED_SORTED = sorted(VIOLENT_CRIME_PROJECTED, key=lambda x: x[2])
    PROPERTY_CRIME_PROJECTED_SORTED = sorted(PROPERTY_CRIME_PROJECTED, key=lambda x: x[2])
    ALL_CRIME_PROJECTED_SORTED = sorted(ALL_CRIME_PROJECTED, key=lambda x: x[2])

    
    with open(SAVE_PATH, "w") as outfile:
        json.dump(ALL_SCORES, outfile)
    
    with open(SAVE_PATH2, "w") as outfile:
        json.dump(VIOLENT_CRIME_SORTED, outfile)
    
    with open(SAVE_PATH3, "w") as outfile:
        json.dump(PROPERTY_CRIME_SORTED, outfile)
    
    with open(SAVE_PATH4, "w") as outfile:
        json.dump(ALL_CRIME_SORTED, outfile)
    
    with open(SAVE_PATH5, "w") as outfile:
        json.dump(VIOLENT_CRIME_PROJECTED_SORTED, outfile)
    
    with open(SAVE_PATH6, "w") as outfile:
        json.dump(PROPERTY_CRIME_PROJECTED_SORTED, outfile)
    
    with open(SAVE_PATH7, "w") as outfile:
        json.dump(ALL_CRIME_PROJECTED_SORTED, outfile)
    
    print("Done!")
    return JsonResponse({"finished": True})

    



def download_newest_crime_data(from_date = 2000, to_date = 2020, save_filepath="./datasets/crime_data.json", agencies_filepath = "./datasets/agencies.json"):
    try:
        f = open(save_filepath)
    except FileNotFoundError:
        CRIME_DATA = {}
    else:
        CRIME_DATA = json.load(f)
    
    f = open(agencies_filepath)
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
        with open(save_filepath, "w") as outfile:
            json.dump(CRIME_DATA, outfile)
        print("Successfully downloaded dataset!")
    except:
        with open(save_filepath, "w") as outfile:
            json.dump(CRIME_DATA, outfile)
        print("Saved what could be saved")

def sort_big_crime_data(CRIME_DATA_PATH = "", SAVE_PATH = "", SAVE_PATH_2 = ""):
    try:
        f = open(CRIME_DATA_PATH)
    except FileNotFoundError:
        print("Crime Data file not found, check the file path!")
        return
    
    SORTED_CRIME_DATA = {}
    SORTED_CRIME_VECTOR = {}

    CRIME_DATA = json.load(f)
    for ORI in CRIME_DATA:
        for result in CRIME_DATA[ORI]["results"]:
            if ORI not in SORTED_CRIME_DATA:
                SORTED_CRIME_DATA[ORI] = {}
            if result["data_year"] not in SORTED_CRIME_DATA[ORI]:
                SORTED_CRIME_DATA[ORI][result["data_year"]] = {}
            SORTED_CRIME_DATA[ORI][result["data_year"]][result["offense"]] = result["actual"]
            if ORI not in SORTED_CRIME_VECTOR:
                SORTED_CRIME_VECTOR[ORI] = {}
            if result["data_year"] not in SORTED_CRIME_VECTOR[ORI]:
                SORTED_CRIME_VECTOR[ORI][result["data_year"]] = [0,0,0,0,0,0,0,0,0,0,0,0]
            SORTED_CRIME_VECTOR[ORI][result["data_year"]][CRIME_TYPE_TO_VECTOR[result["offense"]]] = result["actual"]

    
    with open(SAVE_PATH, "w") as outfile:
        json.dump(SORTED_CRIME_DATA, outfile)
    
    with open(SAVE_PATH_2, "w") as outfile2:
        json.dump(SORTED_CRIME_VECTOR, outfile2)
        print("Successfully sorted crime dataset")
        

def make_ai_vector(SORTED_CRIME_VECTOR_PATH = "", SAVE_PATH = "", SAVE_PATH_2 = ""):
    try:
        f = open(SORTED_CRIME_VECTOR_PATH)
    except FileNotFoundError:
        print("Crime Data file not found, check the file path!")
        return
    SORTED_CRIME_VECTOR = json.load(f)
    big_dict = {}
    x_samples = []
    y_samples = []
    g_samples = []
    g_labels = []
    for ORI in SORTED_CRIME_VECTOR:
        try:
            for i in range(0,16):
                arr1 = []
                issue = False
                for year in range(2000 + i, 2006 + i):
                    if f'{year}' not in SORTED_CRIME_VECTOR[ORI]:
                        issue = True
                if not issue:
                    for year in range(2000 + i, 2005 + i):
                        arr1.append(SORTED_CRIME_VECTOR[ORI][f'{year}'])
                    if not issue:
                        x_samples.append(arr1)
                        y_samples.append(SORTED_CRIME_VECTOR[ORI][f'{2005 + i}'])

            
            arr2 = []
            issue2 = False
            for year in range(2016, 2021):
                try:
                    arr2.append(SORTED_CRIME_VECTOR[ORI][f'{year}'])
                except KeyError:
                    issue2 = True
                    break
            if not issue2:
                g_samples.append(arr2)
                g_labels.append(ORI)
            
        except Exception as e:
            print(e)
            print(f'ORI: {ORI}')
            return
    
    big_dict = {
        "x_samples": x_samples,
        "y_samples": y_samples,
        "g_samples": g_samples,
        "g_labels": g_labels
    }

    x_array = numpy.array(x_samples)
    numpy.save(f'{SAVE_PATH_2}x.npy', x_array)

    y_array = numpy.array(y_samples)
    numpy.save(f'{SAVE_PATH_2}y.npy', y_array)

    g_array = numpy.array(g_samples)
    numpy.save(f'{SAVE_PATH_2}g.npy', g_array)

    g_sample_array = numpy.array(g_labels)
    numpy.save(f'{SAVE_PATH_2}g_label.npy', g_sample_array)
    

    with open(SAVE_PATH, "w") as outfile2:
        json.dump(big_dict, outfile2)
        print("Successfully made arrays")



CRIME_TYPE_TO_VECTOR = {
    "violent-crime": 0,
    "property-crime": 1,
    "rape-legacy": 2,
    "arson": 3,
    "burglary": 4,
    "homicide": 5,
    "human-trafficing": 6,
    "robbery": 7,
    "aggravated-assault": 8,
    "larceny": 9,
    "motor-vehicle-theft": 10,
    "rape": 11
}

def main():
    print(f'Working directory: {os.getcwd()}')
    # download_newest_crime_data(2000, 2020, "./datasets/result.json", "./datasets/agencies.json")
    # sort_big_crime_data("./datasets/crime_data_full.json", "./datasets/crime_data_full_sorted.json", "./datasets/crime_vector_sorted.json")
    # make_ai_vector("./datasets/crime_vector_sorted.json", "./datasets/arrays.json", "./datasets/")
    make_crime_score_dataset()

if __name__ == "__main__":
    main()
