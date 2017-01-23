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
from django.contrib.auth import views
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers

from api.content_api import OutputViewset
from content.views import MashupCreateView, MashupListView, MashupUserListView, MashupDetailView, OutputCreateView,\
                          OutputDetailView, OutputListView, DisplayOutputView, OutputRandomView,\
                          OutputListViewByUser
from bots.views import BotCreateView, BotEditView, BotDetailView, BotAuthorizeView, TweetCreateView, TweetDetailView
from people.views import update_profile, create_profile, UserDetailView, WelcomeView
from sources.views import CorpusCreateView, CorpusListView, CorpusDetailView

# Instantiate Router
router = routers.DefaultRouter()
router.register(r'output', OutputViewset)


urlpatterns = [
    # Root URL
    url(r'^$', OutputListView.as_view()),

    # Admin Area
    url(r'^nothinghere/', admin.site.urls),

    # REST Endpoints
    url(r'^api/', include(router.urls)),

    # Source Management
    url(r'^add_source/$', CorpusCreateView.as_view()),
    url(r'^list_sources/$', CorpusListView.as_view()),
    url(r'^view_source/(?P<pk>\d+)/$', CorpusDetailView.as_view()),

    # Content Generation and Management
    url(r'^create_mashup/$', MashupCreateView.as_view()),
    url(r'^list_mashups/$', MashupListView.as_view()),
    url(r'^my_mashups/$', MashupUserListView.as_view()),
    url(r'^view_mashup/(?P<pk>\d+)/$', MashupDetailView.as_view()),
    url(r'^create_output/$', OutputCreateView),
    url(r'^random/$', OutputRandomView),
    url(r'^view_output/(?P<pk>\d+)/$', OutputDetailView.as_view(), name='output-detail'),
    url(r'^list_output/$', OutputListView.as_view(), name='output-list'),
    url(r'^list_output/(?P<pk>\d+)', OutputListViewByUser.as_view()),

    # Bots - Creation and Management
    url(r'^create_bot/$', BotCreateView.as_view()),
    url(r'^view_bot/(?P<pk>\d+)/$', BotDetailView.as_view(), name='bot-detail'),
    url(r'^authorize_bot/(?P<pk>\d+)/$', BotAuthorizeView.as_view(), name='bot-authorize'),
    url(r'^edit_bot/(?P<pk>\d+)/$', BotEditView.as_view(), name='bot-edit'),

    # Tweets - created by bots app
    url(r'^view_tweet/(?P<pk>\d+)/$', TweetDetailView.as_view(), name='tweet-detail'),
    url(r'^create_tweet/(?P<pk>\d+)/$', TweetCreateView.as_view(), name='tweet-create'),

    # Auth
    url(r'^login/$', views.login, {'template_name': 'people/login.html'}, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^signup/$', create_profile, name='signup'),
    url(r'^edit_profile/$', update_profile, name='update-profile'),
    url(r'^welcome/$', WelcomeView, name='welcome'),
    url(r'^dashboard/$', UserDetailView.as_view(), name='dashboard'),

    # API Endpoints
    url(r'^output/(?P<pk>\d+)/$', DisplayOutputView.as_view()),  # REST API endpoint


]
