from django.shortcuts import render
import requests
from django.http import JsonResponse

def getBoundaries(request, city, state):

    url = f'https://nominatim.openstreetmap.org/search.php?q={city}+{state}+united+states&polygon_geojson=1&format=json'
    r = requests.get(url)
    result = r.json()
    context = []
    p = 0
    for k2 in result:
        if 'boundary' in k2['class']:
            if "MultiPolygon" in k2["geojson"]["type"]:
                
                #for coordinateSection in k2["geojson"]["coordinates"]:
                    #for coordinateSubSection in coordinateSection:
                #    coordinateSubSection = coordinateSection[0]
                #    for k in coordinateSubSection:
                #        context.append( [k[0],k[1]] )
                
                maxLength = -1
                maxIndex = -1
                curIdx = 0
                
                for coordinateSection in k2["geojson"]["coordinates"]: #Goes through all coordinateSections
                    if len(coordinateSection) > maxLength:
                        maxLength = len(coordinateSection)
                        maxIndex = curIdx
                    curIdx += 1
                        
                    #for coordinateSubSection in coordinateSection:
                maxCoordinateSection = k2["geojson"]["coordinates"][maxIndex]
                coordinateSubSection = maxCoordinateSection[0]
                for k in coordinateSubSection:
                    context.append( [k[0],k[1]] )
            
            
            
            
            elif "Polygon" in k2["geojson"]["type"]:
                for coordinate in k2["geojson"]["coordinates"][0]:
                    context.append( [ coordinate[0], coordinate[1] ] )
                
            #for coordinateSection in k2["geojson"]["coordinates"]: #["coordinates"][1][0]
            
            #for k in k2['geojson']['coordinates'][0][0]:
            #    context.append( [k[0],k[1]] )
            
            #for coordinateSection in k2['geojson']['coordinates']:
            #    coordinateSubsection = coordinateSection[0]
            #    for coordinate in coordinateSubsection:
            #        context.append(coordinate[0], coordinate[1])
                

            #for k in coordinateGroup:


    
    return JsonResponse(context, safe = False)
    #return JsonResponse(k2["geojson"], safe = False)