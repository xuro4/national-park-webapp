from django.conf.urls import url
from . import views

app_name = 'parks'

urlpatterns = [
    # home page
    url(r'^$', views.HomePage.as_view(), name='home'),
    # search results
    url(r'^results/$', views.SearchPage.as_view(), name='search-results'),
    # parks detail view
    url(r'^park/(?P<slug>[\w-]+)$',
        views.ParksDetailView.as_view(), name='parks-detail'),
    # news page view
    url(r'^news/(?P<slug>[\w-]+)$',
        views.NewsDetailView.as_view(), name='news-detail'),
    # education page view
    url(r'^education/(?P<slug>[\w-]+)$',
        views.EducationDetailView.as_view(), name='education-detail')

]
