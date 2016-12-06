import random

from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView

from .forms import MashupForm
from .models import Mashup, Output

from extras import mashup_algorithms

# Create your views here.
class MashupCreateView(CreateView):
    """
    Class view for adding a mashup.
    """
    template_name = 'content/create_mashup.html'
    form_class = MashupForm
    success_url = '/list_mashups/'


class MashupListView(ListView):
    model = Mashup

    def get_context_data(self, **kwargs):
        context = super(MashupListView, self).get_context_data(**kwargs)
        return context


class MashupDetailView(DetailView):
    model = Mashup
    context_object_name = 'mashup'
    template_name = 'content/mashup_detail.html'


def OutputCreateView(request):
    """
    FBV for making content from a mashup
    """
    if request.method == 'POST':
        # mashup_id is passed in as a hidden form field
        mashup = Mashup.objects.get(id=request.POST['mashup_id'])


        sentences = list() # Accumulator variable for random sentences to be mashed
        # Get the related corpora for this mashup, then select a random sentence from each
        for corpus in mashup.corpora.all():
            #TODO: remove this breakpoint :)
            #TODO: figure out why this isn't working?
            import ipdb;
            ipdb.set_trace()
            random_sent = random.choice(corpus.sentences.all())
            sentences.append(random_sent.sentence)

        # Hard coded algo lookups based on choice field.. more algorithms will be added here and on the
        # mashup model as they are written
        if mashup.algorithm == 'MJN':
            sent1, sent2 = random.sample(sentences, 2)
            mashed = mashup_algorithms.mouse_join(sent1, sent2)

        outgoing = Output.object.create(body=mashed, mashup=mashup)
        outgoing.save()

        # success_url = reverse_lazy('output:output-detail')

    return render(request, 'content/output_detail.html')

class OutputListView(ListView):
    model = Output
    # TODO: Filter this to only show most recent or top or something like that
    def get_context_data(self, **kwargs):
        context = super(OutputListView, self).get_context_data(**kwargs)
        return context

class OutputDetailView(DetailView):
    model = Output
    context_object_name = 'output'
    template_name = 'content/output_detail.html'



