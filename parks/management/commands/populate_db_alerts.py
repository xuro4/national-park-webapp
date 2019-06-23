from django.core.management.base import BaseCommand, CommandError
from parks.models import Alert
import requests
import logging
from parks.models import Park
from django.conf import settings


class Command(BaseCommand):
    # Updated through Chron Job
    help = 'Populates database with event information for each park'

    def pull_alert_data(self):
        for park in Park.objects.all():
            # API Settings
            endpoint = 'https://developer.nps.gov/api/v1/alerts'
            api_key = str(settings.API_KEY)
            params = {'api_key': api_key,
                      'parkCode': park.slug,
                      'limit': 50}
            # Pull from API 
            response = requests.get(endpoint, params=params).json()
            for entry in response['data']:
                # Populate information with returned JSON Data
                title = entry['title']
                desc = entry['description']
                url = entry['url']
                
                # Save Alert into Database
                new_alert = Alert(title=title, park=park, desc=desc, url=url)
                new_alert.save()

    def remove_all(self):
        Alert.objects.all().delete()

    def handle(self, *args, **options):
        self.remove_all()
        self.pull_alert_data()

