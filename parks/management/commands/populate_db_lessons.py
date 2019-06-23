from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from parks.models import LessonPlans
from parks.models import Park
import requests
import logging


class Command(BaseCommand):
    # Update through Cron Job
    help = 'Populates database with lessons information for each park'

    def pull_lessons_data(self):
        for park in Park.objects.all():
            # API Settings
            endpoint = 'https://developer.nps.gov/api/v1/lessonplans'
            api_key = str(settings.API_KEY)
            params = {'api_key': api_key,
                      'parkCode': park.slug,
                      'limit': 50}
            # Pull from API
            response = requests.get(endpoint, params=params).json()
            for entry in response['data']:
                # Populate Database from Response JSON
                title = entry['title']
                subject_raw = entry['subject']
                # Add a space between commas for formatting
                subject = subject_raw.replace(",", ", ")
                
                # Parse out the duration and remove unnecessary text
                duration_str, space, minute = entry['duration'].partition(" ")
                duration = int(duration_str)

                desc = entry['questionobjective']
                grade = entry['gradelevel']
                url = entry['url']
                
                # if lesson not already in database, add it
                if not LessonPlans.objects.filter(title=title, park=park, subject=subject, duration=duration,
                                                  grade_level=grade, url=url).exists():
                    new_lesson = LessonPlans(title=title, subject=subject, duration=duration, grade_level=grade,
                                             desc=desc, url=url, park=park)
                    new_lesson.save()

    def handle(self, *args, **options):
        self.pull_lessons_data()

