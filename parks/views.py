from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic import ListView
from django.views.generic import DetailView
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Park
from .models import Alert
from .models import Event
from .models import Articles
from .models import NewsReleases
from .models import VisitorCenters
from .models import Campgrounds
from .models import LessonPlans
from .models import People
from .models import Places
from functools import reduce
import operator


# Home Page View
class HomePage(TemplateView):
    template_name = 'parks/home-page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['count'] = Park.objects.count()
        return context


# Search Results Page View
class SearchPage(ListView):
    template_name = 'parks/search-page.html'

    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['page'] = self.request.GET.get('page')
        return context

    def get_queryset(self):
        states = self.request.GET.get('state')
        type = self.request.GET.get('type')
        query = self.request.GET.get('q')

        if states:
            parks = Park.objects.filter(states__icontains=states)
        else:
            parks = Park.objects.all()

        if type == 'PARK':
            parks = parks.filter(Q(designation__icontains='Park') | Q(designation__icontains='Preserve') | Q(designation__icontains='Recreation'))
        elif type == 'TRAIL':
            parks = parks.filter(Q(designation__icontains='Trail') | Q(designation__icontains='Parkway'))
        elif type == 'RIVER':
            parks = parks.filter(Q(designation__icontains='River') | Q(designation__icontains='Lakeshore') | Q(designation__icontains='Seashore'))
        elif type == 'SITE':
            parks = parks.filter(Q(designation__icontains='Site') | Q(designation__icontains='Monument') | Q(designation__icontains='Battlefield')
                                | Q(designation__icontains='Corridor') | Q(designation__icontains='Memorial') | Q(designation__icontains='Heritage Area'))
        elif type == 'OTHER':
            parks = parks.exclude(Q(designation__icontains='Park') | Q(designation__icontains='Preserve') | Q(designation__icontains='Recreation') |
                                  Q(designation__icontains='Trail') | Q(designation__icontains='Parkway') | Q(designation__icontains='River') |
                                  Q(designation__icontains='Lakeshore') | Q(designation__icontains='Seashore') |
                                  Q(designation__icontains='Site') | Q(designation__icontains='Monument') | Q(designation__icontains='Battlefield')
                                  | Q(designation__icontains='Corridor') | Q(designation__icontains='Memorial') | Q(designation__icontains='Heritage Area'))

        result = parks

        if query:
            query_list = query.split()
            result = result.filter(
                reduce(operator.or_, (Q(name__icontains=q) for q in query_list))
            )
        return result


# Location and Geographical Data View
class ParksDetailView(DetailView):
    template_name = 'parks/parks-detail.html'
    model = Park

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        centers_page = self.request.GET.get('centers_page')
        # Visitor Centers split by pages for smoother loading
        centers_list = Paginator(VisitorCenters.objects.filter(park=self.object), 3)
        context['centers'] = centers_list.get_page(centers_page)

        # Complete list of Visitor Centers for map visualization
        context['centers_all'] = VisitorCenters.objects.filter(park=self.object)

        camps_page = self.request.GET.get('camps_page')
        # Campgrounds split by pages for smoother loading
        campgrounds_list = Paginator(Campgrounds.objects.filter(park=self.object), 2)
        context['campgrounds'] = campgrounds_list.get_page(camps_page)

        # Complete list of Campgrounds for map visualization
        context['campgrounds_all'] = Campgrounds.objects.filter(park=self.object)

        return context


# View for Alerts, Events, Articles, etc.
class NewsDetailView(DetailView):
    template_name = 'parks/news-detail.html'
    model = Park

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['alerts'] = Alert.objects.filter(park=self.object)

        events_page = self.request.GET.get('events_page')
        events_list = Paginator(Event.objects.filter(park=self.object), 2)
        context['events'] = events_list.get_page(events_page)

        context['articles'] = Articles.objects.filter(park=self.object)

        news_page = self.request.GET.get('news_page')
        news_list = Paginator(NewsReleases.objects.filter(park=self.object), 2)
        context['news'] = news_list.get_page(news_page)

        articles_page = self.request.GET.get('articles_page')
        articles_list = Paginator(Articles.objects.filter(park=self.object), 3)
        context['articles'] = articles_list.get_page(articles_page)

        return context


# View for LessonPlans and related historical figures/places associated with each Park
class EducationDetailView(DetailView):
    template_name = 'parks/education-detail.html'
    model = Park

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        lessons_page = self.request.GET.get('lessons_page')
        lessons_list = Paginator(LessonPlans.objects.filter(park=self.object), 2)
        context['lessons'] = lessons_list.get_page(lessons_page)

        people_page = self.request.GET.get('people_page')
        people_list = Paginator(People.objects.filter(park=self.object), 2)
        context['people'] = people_list.get_page(people_page)

        places_page = self.request.GET.get('places_page')
        places_list = Paginator(Places.objects.filter(park=self.object), 3)
        context['places'] = places_list.get_page(places_page)

        return context

