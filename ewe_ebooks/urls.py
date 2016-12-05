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
from django.conf.urls import url
from django.contrib import admin
from sources.views import CorpusCreateView, CorpusListView
from content.views import MashupCreateView, MashupListView, MashupDetailVIew


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^add_source/$', CorpusCreateView.as_view()),
    url(r'^list_sources/$', CorpusListView.as_view()),
    url(r'^create_mashup/$', MashupCreateView.as_view()),
    url(r'^list_mashups/$', MashupListView.as_view()),
    url(r'^view_mashup/(?P<pk>\d+)/$', MashupDetailVIew.as_view()),


]
