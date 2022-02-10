from email.policy import default
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
		parser.add_argument('operation', type=str)

	def handle(self, **options):
		if options["operation"] == "update":
			update()
		elif options["operation"] == "clean":
			clean()
		else:
			print("Call with argument \"update\" or \"clean\"")	


def loadCities():
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

def update():
	print('check1')
	cities = loadCities()
	print('check2')
	i = 0
	for city in cities:
		print('check3')
		print(city['city'], city['state'])
		scores = safe_living_score.views.get_score_dict(city["city"], city["state"])
		print('check4')
		city["safelivingscore"] = scores["safe-living-score"]
		print('check5')
		cityapi.updateCity(city["city"], city["state"], **city)
		print('check6')
		if i % 20 == 0:
			print(f"City {i} updated.")
		i += 1
	
	print(f"Updates complete! {i} cities updated.")
		
def clean():
	cities = loadCities()

	cityQueries = City.objects.all()

	for city in cities:
		cityQueries = cityQueries.exclude(name=city["city"], state=city["state"])
	
	leftover = cityQueries.count()
	cityQueries.delete()
	print(f"{leftover} entries deleted.")
	