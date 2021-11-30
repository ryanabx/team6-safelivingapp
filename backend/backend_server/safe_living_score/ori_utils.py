import requests
from requests.sessions import default_headers
import requests_cache
requests_cache.install_cache()
import math
import numbers
import json

"""
How to use:

1. Make an FBI_wrapper(api_key) object
2. Call methods
Useful Methods:
wrapper.getNearestByType(latitude, longitude, type)
wrapper.getAgencies()
wrapper.getAgenciesByCoordinates(latitude, longitude, range)
"""


class RequestCreator:

	def __init__(self, userAPIkey):
		self.userAPIkey = userAPIkey
		self.baseParams = {'api_key': userAPIkey}
		self.BASE_URL = "https://api.usa.gov/crime/fbi/sapi/api/"
		self.regionNameIds = {
			0: "U.S. Territories",
			1: "Northeast",
			2: "Midwest",
			3: "South",
			99: "Other"}
		self.MAX_LONGITUDE = 180
		self.MAX_LATITUDE = 85.05115
	
	def checkValidRegion(self, regionName):
		if type(regionName) == int:
			regionName = self.convertRegionNumberToRegionName(regionName)
			return regionName
		elif type(regionName) == str:
			regionName = self.standardizeRegionName(regionName)
			return regionName
		else:
			raise ValueError("expected regionName to be a string, received " + str(type(regionName)))
	
	def convertRegionNumberToRegionName(self, regionNumber):
		if regionNumber not in self.regionNameIds.keys():
			raise Exception("Provided region number is invalid. Expected 0-4 or 99, received " + str(regionNumber))
		return self.RegionNumToRegionName.get(regionNumber)

	def convertRegionNameToRegionNumber(self, regionName):
		for num, name in self.regionNameIds.items():
			if name == regionName:
				return num
		raise Exception("Provided region name is invalid.")

	def standardizeRegionName(self, regionName):
		match regionName.lower():
			case "u.s. territories":
				return "U.S. Territories"
			case "northwest" :
				return "Northeast"
			case "midwest" :
				return "Midwest"
			case "south" :
				return "South"
			case "west" :
				return "West"
			case "other" :
				return "Other"
			case _:
				raise Exception("regionName not valid")
	
	def haversineDistance(self, latitude1, longitude1, latitude2, longitude2):
		# Radius of Earth in km
		EARTH_RADIUS = 6371
		try:
			self.checkValidCoordinates(latitude1, longitude1)
			self.checkValidCoordinates(latitude2, longitude2)
		except:
			print("How can this happen?")
			print(latitude1, longitude1, latitude2, longitude2)
		latitudeDifference = self.degreesToRadians(latitude2 - latitude1)
		longitudeDifference = self.degreesToRadians(longitude2 - longitude1)

		havTheta = (math.pow(math.sin(latitudeDifference / 2), 2) + 
			math.cos(self.degreesToRadians(latitude1)) * math.cos(self.degreesToRadians(latitude2)) *
			math.pow(math.sin(longitudeDifference / 2), 2) )

		distance = 2 * EARTH_RADIUS * math.asin(math.sqrt(havTheta))
		# in km
		return distance

	def degreesToRadians(self, degrees):
		return degrees * math.pi / 180

	def checkValidRange(self, range):
		if type(range) != int and type(range) != float:
			raise Exception("Expected range to be a number, received " + str(type(range)))
		if range < 0:
			raise Exception("Range cannot be negative")

	def checkValidCoordinates(self, latitude, longitude):
		if not isinstance(longitude, numbers.Number):
			raise Exception("Expected longitue to be a number, received " + str(type(longitude)))
		if not isinstance(latitude, numbers.Number):
			raise Exception("Expected latitude to be a number, received " + str(type(latitude)))
		if abs(latitude) > self.MAX_LATITUDE:
			raise Exception("Latitude beyond valid range")
		if abs(longitude) > self.MAX_LONGITUDE:
			raise Exception("Longitude beyond valid range")

	#def checkNumParameters(numPassedArguments, targetMethod)
	# checkNumParameters
	# checkTypeParameter

	def getAgencies(self, type="default", relevantInfo="", pageNumber=0):
		match type:
			case "default":
				return requests.get(f"{self.BASE_URL}agencies", self.baseParams)
			case "ori":
				params = self.baseParams.copy()
				params['page'] = pageNumber
				return requests.get(f"{self.BASE_URL}agencies/{relevantInfo}", params)
			case "state":
				params = self.baseParams.copy()
				params['page'] = pageNumber
				return requests.get(f"{self.BASE_URL}agencies/byStateAbbr{relevantInfo}", params)
		raise Exception("type must be one of \"default\", \"ori\", or \"state\". Given " + str(type))

	def getStates(self, stateAbbreviation = "", pageNumber = 0):
		params = self.baseParams.copy()
		params['page'] = pageNumber
		return requests.get(f"{self.BASE_URL}states/{stateAbbreviation}", params)

	def getRegions(self, regionName = ""):
		results = requests.get(f"{self.BASE_URL}regions/{regionName}", self.baseParams)
		# DO something if regionName = ""?
		if regionName == "":
			pass
		return results

	def getPoliceEmployment(self, scope = "national", relevantInfo = ""):
		return requests.get(f"{self.BASE_URL}police-employment/{scope}/{relevantInfo}", self.baseParams)

	def getParticipants(self, type, scope, offense, classification, relevantInfo):
		if scope == "national":
			return requests.get(f"{self.BASE_URL}nibrs/{offense}/{type}/{scope}/{classification}", self.baseParams)
		return requests.get(f"{self.BASE_URL}nibrs/{offense}/{type}/{scope}/{relevantInfo}/{classification}", self.baseParams)

	def getCrimeCount(self, scope, offense, relevantInfo=""):
		return self.getParticipants("offense", scope, offense, "count", relevantInfo)

	def getCrimeSummary(self, ori, offense):
		results = requests.get(f"{self.BASE_URL}summarized/agencies/{ori}/{offense}", self.baseParams)
		# DO something if offenses == "offenses"?
		if offense == "offenses":
			pass
		return results

	def getArsonStats(self, scope, relevantInfo = ""):
		results = requests.get(f"{self.BASE_URL}arson/{scope}/{relevantInfo}", self.baseParams)
		return results

	def getAgencyParticipation(self, scope, relevantInfo=""):
		results = requests.get(f"{self.BASE_URL}participation/{scope}/{relevantInfo}", self.baseParams)
		return results

	def getEstimates(self, scope, relevantInfo=""):
		results = requests.get(f"{self.BASE_URL}estimates/{scope}/{relevantInfo}", self.baseParams)
		return results	

#######################################################################
#######################################################################

class FBI_wrapper:
	NATIONAL_SCOPE = "national"
	REGIONAL_SCOPE = "regions"
	STATE_SCOPE = "states"
	ORI_SCOPE = "agencies"

	def __init__(self):
		self.api_key = 'nHym62MTPDELS0XgtAZLLw0fL3jNWoNvsY2kn315'
		self.rc = RequestCreator(self.api_key)
	
	def getAgencies(self):
		"""
		Gets information about all agencies in the United States.
		"""
		message = self.rc.getAgencies()
		data = message.json()
		result = []
		for stateName in data:
			state = data[stateName]
			for agencyName in state:
				result.append(state[agencyName].copy())
		return result

	def getAgenciesByCoordinates(self, latitude, longitude, range = 50):
		self.rc.checkValidRange(range)
		self.rc.checkValidCoordinates(latitude, longitude)

		response = self.rc.getAgencies()
		data = response.json()

		agencies = []
		for stateName in data.keys():
			state = data[stateName]
			for agencyName in state.keys():
				agency = state[agencyName]
				if not isinstance(agency["latitude"], numbers.Number) and not isinstance(agency["longitude"], numbers.Number):
					# If the Agency does not have a Longitude/Latitude... we ignore it.
					pass
				else:
					agency = agency.copy()
					agency["distance"] = self.rc.haversineDistance(latitude, longitude, agency["latitude"], agency["longitude"])
					if agency["distance"] <= range:
						agencies.append(agency)
		return agencies

	# Types include... "City", "County", "Other State Agency", 
	def getNearestByType(self, latitude, longitude, type="Any"):
		self.rc.checkValidCoordinates(latitude, longitude)

		message = self.rc.getAgencies()
		data = message.json()
		
		allowAny = type == "Any"

		agencies = []
		minDistance = float('inf')

		for stateName in data.keys():
			state = data[stateName]
			for agencyName in state.keys():
				agency = state[agencyName]
				if allowAny or type == agency["agency_type_name"]:
					if not isinstance(agency["latitude"], numbers.Number) and not isinstance(agency["longitude"], numbers.Number):
						# If the Agency does not have a Longitude/Latitude... we ignore it.
						pass
					else:
						dist = self.rc.haversineDistance(latitude, longitude, agency["latitude"], agency["longitude"])
						agency = agency.copy()
						agency["distance"] = dist
						if dist == minDistance:
							agencies.append(agency.copy())
						elif dist < minDistance:
							agencies = [agency.copy()]
							minDistance = dist
		return agencies

	def getAgenciesByRegion(self, regionName):
		regionName = self.rc.checkValidRegion(regionName)

		allRegions = (regionName == "U.S. Territories")

		message = self.rc.getAgencies()
		data = message.json()

		agencies = []
		for stateName in data.keys():
			state = data[stateName]
			print(len(state))
			for agencyName in state.keys():
				if allRegions or (state[agencyName]["regionName"] is not None and state[agencyName]["regionName"] == regionName):
					agencies.append(state[agencyName])
		return agencies

	def getAgenciesByState(self, stateAbreviation, pageNumber = 0):
		message = self.rc.getAgencies("state", stateAbreviation, pageNumber)
		data = message.json()
		return data

	def getAgencyByORI(self, ori):
		message = self.rc.getAgencies("ori", ori)
		data = message.json()
		return data

	def getStates(self, pageNumber = 0):
		message = self.rc.getStates("", pageNumber)
		data = message.json()
		return data

	def getAllStates(self):
		message0 = self.getStates()
		data0 = message0.json()
		states = [].extend(data0)
		for i in data0["pagination"]["pages"]:
			messagei = self.getStates(i)
			datai = messagei.json()
			states.extend(datai)
		return states

	#def getStatesByRegion(self, regionName):
	#	regionName = self.rc.convertRegionNameToRegionNumber(regionName)
	#	dataList = self.getAllStates()
		#if
		
if __name__ == "__main__":
	api_key = "nHym62MTPDELS0XgtAZLLw0fL3jNWoNvsY2kn315"

	# fbi = FBI_wrapper(api_key)
	fbi = FBI_wrapper()
	# test = fbi.getAgenciesByCoordinates(36.5, -85.0)
	# test = fbi.getNearestByType(101.8552, 33.5779, "City")
	test = fbi.getNearestByType(33.5779, -101.8551665, "City")
	print(len(test))
	for i in range(min(20, len(test))):
		print(test[i])
