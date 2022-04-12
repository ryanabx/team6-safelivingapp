import numpy
import json

def get_crime_data(year_count = 5):
    with open('') as crime_file:
        crime_data = json.load(crime_file)    
        data_vects = []
        for ori, ori_data in ori_data.items():
            annual_vects = []
            years = []
            for year, year_data in crime_data.items():
                v = numpy.array(year_data.values())
                annual_vects[year] = v
                years.append(year)
            for year in years:
                if not set(range(year, year + year_count)).issubset(set(years)):
                    continue
                v = []
                for year in range(year, year + year_count):
                    v.append(annual_vects[year])
                data_vects.append(v)
            





