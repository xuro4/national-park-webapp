from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from parks.models import People
from parks.models import Park
import requests
import logging


class Command(BaseCommand):
    help = 'Populates database with event information for each park'

    def pull_people_data(self):
        for park in Park.objects.all():
            endpoint = 'https://developer.nps.gov/api/v1/people'
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

                if not People.objects.filter(title=title, park=park, img=img, desc=desc, url=url).exists():
                    new_person = People(title=title, park=park, img=img, desc=desc, url=url)
                    new_person.save()

    def handle(self, *args, **options):
        self.pull_people_data()

