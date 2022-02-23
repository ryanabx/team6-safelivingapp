from django.shortcuts import render
import requests
from django.http import JsonResponse
import json

def get_crime_data_old(agency, fromDate, toDate):
    #agency = 'FL0500500'
    #fromDate = '2019'
    #toDate = '2020'
    if(toDate < fromDate):
        tempDate = fromDate
        fromDate = toDate
        toDate = tempDate
    if(toDate > 2020 or fromDate > 2020 or toDate < 2000 or fromDate < 2000):
        return_value = {
            'message': 'Please provide a valid date range (2000 to 2020)'
        }
        return JsonResponse(return_value)
    key = 'nHym62MTPDELS0XgtAZLLw0fL3jNWoNvsY2kn315'
    url = f'https://api.usa.gov/crime/fbi/sapi//api/summarized/agencies/{agency}/offenses/{fromDate}/{toDate}?api_key={key}'
    #url = f'https://api.usa.gov/crime/fbi/sapi/api/nibrs/offenses/agencies/{agency}?api_key={key}'
    r = requests.get(url)
    stuff = r.json()
    stuff["error_code"] = 0
    stuff["error_message"] = ""
    return stuff

def api_get_crime_data(request, agency, fromDate = 2020, toDate = 2020):
    return JsonResponse(get_crime_data(agency, fromDate, toDate))

# Retrieves FBI Crime Data Explorer Crime Data, or local dataset if the date range is 2020-2020
def get_crime_data(agency, fromDate = 2020, toDate = 2020):
    if toDate < fromDate:
        return {"error_code": 1, "error_message": "To date cannot be lower than from date."}
    if toDate > 2020 or fromDate > 2020 or toDate < 2000 or fromDate < 2000:
        return {"error_code": 2, "error_message": "Invalid date range. Dates must be between 2000 and 2020."}
    
    if fromDate == 2020 and toDate == 2020:
        CRIME_DATA = json.load(open('./datasets/crime_data_sorted.json'))
        if agency[0:2] in CRIME_DATA:
            if agency in CRIME_DATA[agency[0:2]]:
                results = CRIME_DATA[agency[0:2]][agency]
                results["error_code"] = 0
                results["error_message"] = ""
                return results
            else:
                return {"error_code": 3, "error_message": "Agency does not exist."}
        elif agency[0:2] == "NB":
            if agency in CRIME_DATA["NE"]:
                results = CRIME_DATA["NE"][agency]
                results["error_code"] = 0
                results["error_message"] = ""
                return results
            else:
                return {"error_code": 3, "error_message": "Agency does not exist."}
        else:
            return {"error_code": 3, "error_message": "Agency does not exist."}
    else:
        return get_crime_data_old(agency, fromDate, toDate)
