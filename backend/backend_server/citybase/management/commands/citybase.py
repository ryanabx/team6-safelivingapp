from email.policy import default
import time
from citybase.models import City
from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers
from django.core.management.base import BaseCommand
import sys
import json
import safe_living_score.views
import citybase.cityapi as cityapi

class Command(BaseCommand):
	help = "Updates city data"

	import argparse

	def add_arguments(self, parser: argparse.ArgumentParser):
		parser.description = "Updates city data. Use \"update\" or \"clean\""
		parser.add_argument('operation', type=str, choices=["update", "clean", "clear"])
		parser.add_argument('--v', action="store_true")

	def handle(self, **options):
		verbose = options['v']
		if options["operation"] == "update":
			update(verbose)
		elif options["operation"] == "clean":
			clean(verbose)
		elif options["operation"] == "clear":
			clear(verbose)
		else:
			print("Call with argument \"update\", \"clean\", or \"clear\"")	

def loadCities_old():
	states = json.load(open("datasets/population_data_fixed.json"))
	cities = []
	for state, c in states.items():
		for cityname, citypop in c.items():
			cities.append({
				"city": cityname, 
				"state": state,
				"population": citypop["Population"]
			})
	return cities

def loadCities():
	cities = json.load(open("datasets/us_city_info.json"))
	for city in cities:
		city["state"] = city["state_id"]
	return cities

def update_old(verbose):
	cities = loadCities()
	total = len(cities)
	i = 0
	percent = 0
	start_time = time.time()
	last_i_time = start_time
	this_i_time = 0
	POPULTION_DATA = json.load(open('./datasets/population_data_fixed.json'))
	CRIME_DATA = json.load(open('./datasets/crime_data_sorted.json'))

	for city in cities:
		if verbose:
			this_i_time = time.time()
			seconds = this_i_time - start_time
			print(f"{i:5}/{total:5} {int(seconds/3600):02}:{int((seconds/60)%60):02}:{int(seconds%60):02} Adding {city['city']}, {city['state']}")
			last_i_time = this_i_time
		elif int(i*100/total) > percent:
			percent = int(i*100/total)
			this_i_time = time.time()
			seconds = this_i_time - start_time
			print(f"{int(i*100/total):3}% {int(seconds/3600):02}:{int((seconds/60)%60):02}:{int(seconds%60):02}")
			last_i_time = this_i_time
		scores = safe_living_score.views.get_safe_living_score(city["city"], city["state"], POPULATION_DATA=POPULTION_DATA, CRIME_DATA=CRIME_DATA)
		city["safelivingscore"] = scores["safe-living-score"]
		cityapi.updateCity(**city)
		i += 1
	
	print(f"Updates complete! {i} cities updated.")
		
def clean(verbose):
	cities = loadCities()
	total = len(cities)
	i = 0
	percent = 0
	start_time = time.time()
	last_i_time = start_time
	this_i_time = 0

	cityQueries = City.objects.all()
	current_cities = list(cityQueries)

	for city in cities:
		if verbose:
			this_i_time = time.time()
			seconds = this_i_time - start_time
			print(f"{i:5}/{total:5} {int(seconds/3600):02}:{int((seconds/60)%60):02}:{int(seconds%60):02} Checking {city['city']}, {city['state']}")
			last_i_time = this_i_time
		elif int(i*100/total) > percent:
			percent = int(i*100/total)
			this_i_time = time.time()
			seconds = this_i_time - start_time
			print(f"{int(i*100/total):3}% {int(seconds/3600):02}:{int((seconds/60)%60):02}:{int(seconds%60):02}")
			last_i_time = this_i_time
		cityQuery = list(City.objects.all().filter(name=city["city"], state=city["state"]))
		for c in cityQuery:
			current_cities.remove(c)
		i += 1
	
	leftover = len(current_cities)
	for c in current_cities:
		print(f"Deleting {c.name}, {c.state}")
		c.delete()
	
	print(f"{leftover} entries deleted.")
	
def clear(verbose):
	total = City.objects.all().count()
	start_time = time.time()
	this_i_time = 0

	cityQueries = City.objects.all()
	print(f"Deleting {total} cities")
	cityQueries.delete()
	this_i_time = time.time()
	seconds = this_i_time - start_time
	print(f"Clear finished. Took {int(seconds/3600):02}:{int((seconds/60)%60):02}:{int(seconds%60):02}")

def update(verbose):
	cities = loadCities()
	total = len(cities)
	i = 0
	percent = 0
	start_time = time.time()
	last_i_time = start_time
	this_i_time = 0
	POPULTION_DATA = json.load(open('./datasets/population_data_fixed.json'))
	CRIME_DATA = json.load(open('./datasets/crime_data_sorted.json'))

	for city in cities:
		if verbose:
			this_i_time = time.time()
			seconds = this_i_time - start_time
			print(f"{i:5}/{total:5} {int(seconds/3600):02}:{int((seconds/60)%60):02}:{int(seconds%60):02} Adding {city['city']}, {city['state']}")
			last_i_time = this_i_time
		elif int(i*100/total) > percent:
			percent = int(i*100/total)
			this_i_time = time.time()
			seconds = this_i_time - start_time
			print(f"{int(i*100/total):3}% {int(seconds/3600):02}:{int((seconds/60)%60):02}:{int(seconds%60):02}")
			last_i_time = this_i_time
		scores = safe_living_score.views.get_safe_living_score(city["city"], city["state"], POPULATION_DATA=POPULTION_DATA, CRIME_DATA=CRIME_DATA)
		city["safelivingscore"] = scores["safe-living-score"]
		city["latitude"] = city["lat"]
		city["longitude"] = city["lng"]
		city.pop("state_id")
		city.pop("county_name")
		city.pop("lat")
		city.pop("lng")
		city.pop("density")
		cityapi.updateCity(**city)
		i += 1
	print(f"Updates complete! {i} cities updated.")

def dbsize(verbose):
	size = City.objects.all().count()
	print(f"{size} cities are in the database.")
