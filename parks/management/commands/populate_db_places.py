from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from parks.models import Places
from parks.models import Park
import requests
import logging


class Command(BaseCommand):
    help = 'Populates database with event information for each park'

    def pull_places_data(self):
        for park in Park.objects.all():
            endpoint = 'https://developer.nps.gov/api/v1/places'
            api_key = str(settings.API_KEY)
            params = {'api_key': api_key,
                      'parkCode': park.slug,
                      'limit': 50}

            response = requests.get(endpoint, params=params).json()
            for entry in response['data']:
                title = entry['title']
                img = entry['listingimage']['url']
                desc = entry['listingdescription']
                url = entry['url']

                if not Places.objects.filter(title=title, park=park, img=img, desc=desc, url=url).exists():
                    new_place = Places(title=title, park=park, img=img, desc=desc, url=url)
                    new_place.save()

    def handle(self, *args, **options):
        self.pull_places_data()

