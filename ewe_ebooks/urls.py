"""ewe_ebooks URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from sources.views import CorpusCreateView, CorpusListView, CorpusDetailView, CorpusUpdateView
from content.views import MashupCreateView, MashupListView, MashupDetailView, OutputCreateView,\
                          OutputDetailView, OutputListView, DisplayOutputView, OutputRandomView

from rest_framework import routers
from api.content_api import OutputViewset

# Instantiate Router
router = routers.DefaultRouter()
router.register(r'output', OutputViewset)


urlpatterns = [
    # Admin Area
    url(r'^admin/', admin.site.urls),

    # REST Endpoints
    url(r'^api/', include(router.urls)),

    # Source Management
    url(r'^add_source/$', CorpusCreateView.as_view()),
    url(r'^list_sources/$', CorpusListView.as_view()),
    url(r'^view_source/(?P<pk>\d+)/$', CorpusDetailView.as_view()),

    # Content Generation and Management
    url(r'^create_mashup/$', MashupCreateView.as_view()),
    url(r'^list_mashups/$', MashupListView.as_view()),
    url(r'^view_mashup/(?P<pk>\d+)/$', MashupDetailView.as_view()),
    url(r'^create_output/$', OutputCreateView),
    url(r'^random/$', OutputRandomView),
    url(r'^view_output/(?P<pk>\d+)/$', OutputDetailView.as_view(), name='output-detail'),
    url(r'^output/(?P<pk>\d+)/$', DisplayOutputView.as_view()),  # REST API endpoint
    url(r'^list_output/$', OutputListView.as_view(), name='output-list'),



]
