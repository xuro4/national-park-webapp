from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.geos.point import Point
from django.conf import settings
from parks.models import Campgrounds
from parks.models import Park
import requests
import logging


class Command(BaseCommand):
    # Updated through Cron Job
    help = 'Populates database with campground information for each park'

    def pull_campground_data(self):
        for park in Park.objects.all():
            # API Settings
            endpoint = 'https://developer.nps.gov/api/v1/campgrounds'
            api_key = str(settings.API_KEY)
            params = {'api_key': api_key,
                      'parkCode': park.slug,
                      'limit': 100}
            # Pull from API
            response = requests.get(endpoint, params=params).json()
            for entry in response['data']:
                # fill in background info
                name = entry['name']
                desc = entry['description']
                weather = entry['weatheroverview']
                reg_overview = entry['regulationsoverview']
                try:
                    campsites = int(entry['campsites']['totalsites'])
                except KeyError:
                    campsites = int(entry['campsites']['totalSites'])

                reserve_url = entry['reservationsurl']

                # fill in accessibility info
                internet_info = entry['accessibility']['internetinfo']
                rv_info = entry['accessibility']['rvinfo']
                ada_info = entry['accessibility']['adainfo']
                wheelchair_info = entry['accessibility']['wheelchairaccess']
                cell_info = entry['accessibility']['cellphoneinfo']
                add_info = entry['accessibility']['additionalinfo']

                # fill in requirements/amenity info
                firewood_str = entry['amenities']['firewoodforsale']
                if firewood_str != "No" and firewood_str != "":
                    firewood = True
                else:
                    firewood = False

                ice_str = entry['amenities']['iceavailableforsale']
                if ice_str != "No" and ice_str != "":
                    ice = True
                else:
                    ice = False

                food_str = entry['amenities']['foodstoragelockers']
                if food_str != "No" and food_str != "":
                    food_storage = True
                else:
                    food_storage = False

                internet_str = entry['amenities']['internetconnectivity']
                if internet_str != "No" and internet_str != "":
                    internet = True
                else:
                    internet = False

                cell_str = entry['amenities']['cellphonereception']
                if cell_str != "No" and cell_str != "":
                    cellphone = True
                else:
                    cellphone = False

                # Parse through data for geographical information, filtering out commas and other unnecessary characters
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
                
                # If campground doesn't exist, add it to the database
                if not Campgrounds.objects.filter(name=name, park=park, geometry=point, desc=desc).exists():
                    new_campground = Campgrounds(name=name, park=park, reserve_url=reserve_url, desc=desc, weather=weather,
                                                 reg_overview=reg_overview, campsites=campsites,
                                                 internet_info=internet_info, rv_info=rv_info, ada_info=ada_info,
                                                 wheelchair_info=wheelchair_info, cell_info=cell_info, additional_info=add_info,
                                                 firewood=firewood, ice=ice, food_storage=food_storage,
                                                 internet=internet, cellphone=cellphone, geometry=point)
                    new_campground.save()

    def handle(self, *args, **options):
        self.pull_campground_data()
