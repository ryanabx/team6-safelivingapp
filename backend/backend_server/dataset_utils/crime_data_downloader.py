# Utility function to download the newest crime data from the FBI Crime Data Explorer
import json
import requests
import os
import numpy

CRIME_DATA_EXPLORER_KEY = json.load(open('./API_KEYS.json'))["crime_data_explorer"]


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
    make_ai_vector("./datasets/crime_vector_sorted.json", "./datasets/arrays.json", "./datasets/")

if __name__ == "__main__":
    main()
