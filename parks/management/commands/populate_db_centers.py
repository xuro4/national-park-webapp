from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.geos.point import Point
from django.conf import settings
from parks.models import VisitorCenters
from parks.models import Park
import requests
import logging


class Command(BaseCommand):
    help = 'Populates database with visitor center information for each park'

    def pull_center_data(self):
        for park in Park.objects.all():
            endpoint = 'https://developer.nps.gov/api/v1/visitorcenters'
            api_key = str(settings.API_KEY)
            params = {'api_key': api_key,
                      'parkCode': park.slug,
                      'limit': 50}

            response = requests.get(endpoint, params=params).json()
            for entry in response['data']:
                name = entry['name']
                desc = entry['description']
                directions = entry['directionsInfo']
                direction_url = entry['directionsUrl']
                url = entry['url']

                if entry['latLong'] != '':
                    lat_shard, comma, long_shard = entry['latLong'].partition(', ')
                    lat_str = lat_shard.replace('{lat:', '')
                    long_str_first_pass = long_shard.replace('lng:', '')
                    long_str = long_str_first_pass.replace('}', '')

                    lat = float(lat_str)
                    long = float(long_str)
                    point = Point(long, lat)
                else:
                    point = None

                if not VisitorCenters.objects.filter(name=name, geometry=point, direction_url=direction_url, url=url).exists():
                    new_center = VisitorCenters(name=name, geometry=point, direction_url=direction_url, url=url, park=park,
                                                desc=desc, directions=directions)
                    new_center.save()

    def handle(self, *args, **options):
        self.pull_center_data()

