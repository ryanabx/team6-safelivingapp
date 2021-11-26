from django.shortcuts import render
import requests
from django.http import JsonResponse
from django.http import response

# Create your views here.
def getGeocoding(request, inputAddr):
    key = 'c7qYTGBjRaRkGF7ucqOvpNy6L1Q857oD'
    addrList = []

    #print(type(inputAddr)) # note, inputAddr always comes in as a string :(
    #print(inputAddr)

    # if '|' exists in incoming addr string, there are multple requested addresses
    # if not, its a single address request
    if ("|" in inputAddr) :
        
        inputAddr = list(inputAddr)
        addr = ''
        url = f'http://www.mapquestapi.com/geocoding/v1/batch?key={key}'

        #print(len(inputAddr))
        # iterate through chars in inputAddr string
        for i in range(len(inputAddr)):

            # build individual addrs from string between break chars, 
            # # when a '|' is hit, add that built address to the list, reset the addr string
            # if its the last char of string, finish building addr then add to list
            if (inputAddr[i] != '|') :
                #print (inputAddr[i])
                #print (inputAddr.index(c))
                addr = addr + inputAddr[i]
                if (i == len(inputAddr) - 1):
                    addrList.append(addr)
                    addr = '' 
            elif (inputAddr[i] == '|'):
                addrList.append(addr)
                addr = ''
        
        #print(addrList)
        #print(type(addrList[1]))

        # build the url for each address taken from string
        for addr in addrList:
            url = url + '&location=' + addr
    else:

        # string for single address if no '|' exists
        url = f'http://www.mapquestapi.com/geocoding/v1/address?key={key}&location={inputAddr}'
        
    # perform api call with constructed url
    #print (url)
    r = requests.get(url)
    stuff = r.json()
    return JsonResponse(stuff)
