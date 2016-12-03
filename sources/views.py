from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.views.generic import ListView
from .forms import CorpusForm
from extras.twittstopher import Timeline

# Create your views here!

class CorpusCreateView(CreateView):
    """
    View for adding a and processing a source (corpus)
    """
    template_name = 'sources/create_corpus.html'
    form_class = CorpusForm
    success_url = '/view_sources/'


class CorpusListView(ListView):
    pass

