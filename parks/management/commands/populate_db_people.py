from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from parks.models import People
from parks.models import Park
import requests
import logging


class Command(BaseCommand):
    help = 'Populates database with people information for each park'

    def pull_people_data(self):
        for park in Park.objects.all():
            # API Settings
            endpoint = 'https://developer.nps.gov/api/v1/people'
            api_key = str(settings.API_KEY)
            params = {'api_key': api_key,
                      'parkCode': park.slug,
                      'limit': 50}
            # Pull from API
            response = requests.get(endpoint, params=params).json()
            for entry in response['data']:
                # Populate Database from Response JSON
                title = entry['title']
                img = entry['listingimage']['url']
                desc = entry['listingdescription']
                url = entry['url']

                # If person isn't already in database, add them
                if not People.objects.filter(title=title, park=park, img=img, desc=desc, url=url).exists():
                    new_person = People(title=title, park=park, img=img, desc=desc, url=url)
                    new_person.save()

    def handle(self, *args, **options):
        self.pull_people_data()

