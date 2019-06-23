from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from parks.models import Articles
from parks.models import Park
import requests
import logging


class Command(BaseCommand):
    help = 'Populates database with event information for each park'

    def pull_article_data(self):
        for park in Park.objects.all():
            endpoint = 'https://developer.nps.gov/api/v1/articles'
            api_key = str(settings.API_KEY)
            params = {'api_key': api_key,
                      'parkCode': park.slug,
                      'limit': 50}

            response = requests.get(endpoint, params=params).json()
            for entry in response['data']:
                title = entry['title']
                desc = entry['listingdescription']

                url = entry['url']

                image_url = entry['listingimage']['url']
                if image_url == "":
                    image_url = 'https://i.redd.it/fuq4v4hvt1n21.jpg'

                if not Articles.objects.filter(title=title, park=park, desc=desc, url=url).exists():
                    new_article = Articles(title=title, park=park, desc=desc, url=url, img=image_url)
                    new_article.save()

    def handle(self, *args, **options):
        self.pull_article_data()

