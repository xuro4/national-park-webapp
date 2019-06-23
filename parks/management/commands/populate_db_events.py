from django.core.management.base import BaseCommand, CommandError
from parks.models import Event
import requests
import logging
from parks.models import Park
import datetime
from bs4 import BeautifulSoup
from django.conf import settings


class Command(BaseCommand):
    help = 'Populates database with event information for each park'

    def pull_event_data(self):
        today = datetime.date.today()
        for park in Park.objects.all():
            endpoint = 'https://developer.nps.gov/api/v1/events'
            api_key = str(settings.API_KEY)
            params = {'api_key': api_key,
                      'parkCode': park.slug,
                      'limit': 50}

            response = requests.get(endpoint, params=params).json()
            for entry in response['data']:
                title = entry['title']

                date_start_str = entry['datestart']
                date_start = datetime.datetime.strptime(date_start_str, '%Y-%m-%d').date()
                date_end_str = entry["dateend"]
                date_end = datetime.datetime.strptime(date_end_str, '%Y-%m-%d').date()

                times = []
                for time in entry['times']:
                    start = time["timestart"]
                    end = time["timeend"]
                    time_str = start + " - " + end
                    times.append(time_str)

                desc_raw = entry['description']
                soup = BeautifulSoup(desc_raw)
                desc = soup.get_text()

                reg_required = entry['isregresrequired']
                reg = bool(reg_required)
                reg_info = entry['regresinfo']

                if date_end >= today and not Event.objects.filter(title=title, date_start=date_start, date_end=date_end,
                                                                  park=park, desc=desc, reg_required=reg).exists():
                    new_event = Event(title=title, date_start=date_start, date_end=date_end, park=park,
                                      times=times, desc=desc, reg_required=reg, reg_info=reg_info)
                    new_event.save()

    def remove_concluded_events(self):
        today = datetime.date.today()
        for event in Event.objects.all():
            if event.date_end < today:
                event.delete()

    def handle(self, *args, **options):
        self.remove_concluded_events()
        self.pull_event_data()

