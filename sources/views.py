from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.views.generic import ListView
from .forms import CorpusForm
from .models import Corpus

# Create your views here!

class CorpusCreateView(CreateView):
    """
    View for adding a and processing a source (corpus)
    """
    template_name = 'sources/create_corpus.html'
    form_class = CorpusForm
    success_url = '/list_sources/'


class CorpusListView(ListView):
    model = Corpus

    def get_context_data(self, **kwargs):
        context = super(CorpusListView, self).get_context_data(**kwargs)
        return context


