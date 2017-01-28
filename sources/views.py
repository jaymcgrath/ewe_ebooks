from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.views.generic import ListView, DetailView, UpdateView
from .forms import CorpusForm
from .models import Corpus

from extras.mixins import VerifiedEmailRequiredMixin

# Create your views here!


class CorpusCreateView(VerifiedEmailRequiredMixin, CreateView):
    """
    View for adding a and processing a source (corpus)
    """
    template_name = 'sources/create_corpus.html'
    form_class = CorpusForm
    success_url = '/list_sources/'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super(CorpusCreateView, self).form_valid(form)


class CorpusListView(ListView):
    model = Corpus
    queryset = Corpus.objects.order_by('-updated')
    # context_object_name = 'corpus_list'
    paginate_by = 25

    def get_context_data(self, **kwargs):
        context = super(CorpusListView, self).get_context_data(**kwargs)
        return context


class CorpusDetailView(DetailView):
    """
    View for individual corpus (will have a refresh button)
    """
    model = Corpus
    context_object_name = 'corpus'


class CorpusUpdateView(UpdateView):
    """
    View for freshening an individual corpus
    """
    model = Corpus
    pass

