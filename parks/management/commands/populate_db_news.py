from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from parks.models import NewsReleases
from parks.models import Park
import requests
import logging
import datetime


class Command(BaseCommand):
    help = 'Populates database with event information for each park'

    def pull_news_data(self):
        for park in Park.objects.all():
            endpoint = 'https://developer.nps.gov/api/v1/newsreleases'
            api_key = str(settings.API_KEY)
            params = {'api_key': api_key,
                      'parkCode': park.slug,
                      'limit': 50}

            response = requests.get(endpoint, params=params).json()
            for entry in response['data']:
                title = entry['title']

                date_str = entry['releasedate']
                date = datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S.%f').date()

                abstract = entry['abstract']
                url = entry['url']
                img_url = entry['image']['url']

                if img_url == "":
                    img_url = 'https://iamuniversity-5f58.kxcdn.com/wp-content/uploads/2017/04/670_shutterstock_1157773241.jpg'
                if not NewsReleases.objects.filter(title=title, date=date, park=park,
                                                   abstract=abstract, url=url).exists():
                    new_news = NewsReleases(title=title, date=date, park=park, img=img_url, abstract=abstract, url=url)
                    new_news.save()

    def handle(self, *args, **options):
        self.pull_news_data()

