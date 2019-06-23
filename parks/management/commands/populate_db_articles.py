from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from parks.models import Articles
from parks.models import Park
import requests
import logging


class Command(BaseCommand):
    # Updated through Cron Job
    help = 'Populates database with event information for each park'

    def pull_article_data(self):
        for park in Park.objects.all():
            # API settings
            endpoint = 'https://developer.nps.gov/api/v1/articles'
            api_key = str(settings.API_KEY)
            params = {'api_key': api_key,
                      'parkCode': park.slug,
                      'limit': 50}
            
            # Pull from API
            response = requests.get(endpoint, params=params).json()
            for entry in response['data']:
                # Populate information based on returned JSON
                title = entry['title']
                desc = entry['listingdescription']

                url = entry['url']

                image_url = entry['listingimage']['url']
                # If no image provided use a default
                if image_url == "":
                    image_url = 'https://i.redd.it/fuq4v4hvt1n21.jpg'
                # If Article not already present in database, save it
                if not Articles.objects.filter(title=title, park=park, desc=desc, url=url).exists():
                    new_article = Articles(title=title, park=park, desc=desc, url=url, img=image_url)
                    new_article.save()

    def handle(self, *args, **options):
        self.pull_article_data()

