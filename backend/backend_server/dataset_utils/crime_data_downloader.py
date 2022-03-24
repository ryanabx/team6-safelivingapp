# Utility function to download the newest crime data from the FBI Crime Data Explorer
import json
import requests
import os

CRIME_DATA_EXPLORER_KEY = 'nHym62MTPDELS0XgtAZLLw0fL3jNWoNvsY2kn315'


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
    except KeyboardInterrupt:
        with open(save_filepath, "w") as outfile:
            json.dump(CRIME_DATA, outfile)
        print("Saved what could be saved")

def main():
    print(f'Working directory: {os.getcwd()}')
    download_newest_crime_data(2000, 2020, "./agencies.json", "./result.json")

if __name__ == "__main__":
    main()
