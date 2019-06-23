from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.geos.point import Point
from django.utils.text import slugify
from parks.models import Park
from django.conf import settings
import requests
import logging


class Command(BaseCommand):
    # Update using Cron Job
    help = 'Populates database with National Park information'

    def pull_park_data(self, start_index):
        # API Settings
        endpoint = 'https://developer.nps.gov/api/v1/parks'
        api_key = str(settings.API_KEY)
        params = {'api_key': api_key,
                  'parkCode': '',
                  'limit': 100,
                  'start': start_index}
        # Pull from API
        response = requests.get(endpoint, params=params).json()
        for entry in response['data']:
            # Populate Database from API entries
            name_special_charas = entry['name']
            
            # Replace specific characters that won't display properly with rough equivalents
            name_stripped_first_pass = name_special_charas.replace('&#333;', 'o')
            name_stripped_second_pass = name_stripped_first_pass.replace('&#241;', 'n')
            name = name_stripped_second_pass.replace('&#257;', 'a')

            states = entry['states']
            park_code_str = entry['parkCode']
            slug = slugify(park_code_str)
            desc = entry["description"]
            designation = entry['designtaion']
            
            # Parse through latLong return to remove unnecessary characters
            if entry['latLong'] != '':
                lat_shard, comma, long_shard = entry['latLong'].partition(', ')
                lat_str = lat_shard.replace('lat:', '')
                long_str = long_shard.replace('long:', '')

                lat = float(lat_str)
                long = float(long_str)
                point = Point(long, lat)
            else:
                point = None
            
            # If park doesn't already exist, add it to the database
            if not Park.objects.filter(name=name, states=states, slug=slug, geometry=point).exists():
                new_park = Park(name=name, states=states, slug=slug, geometry=point, desc=desc, designation=designation)
                new_park.save()

    def handle(self, *args, **options):
        self.pull_park_data(1)
        self.pull_park_data(101)
        self.pull_park_data(201)
        self.pull_park_data(301)
        self.pull_park_data(401)
        self.pull_park_data(501)
