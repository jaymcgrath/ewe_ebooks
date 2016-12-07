import random

from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from django.db.models import F


from .forms import MashupForm
from .models import Mashup, Output
from sources.models import Corpus

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

        # Create container for random slices of sentences
        corpus_samples = list()

        for corpus in mashup.corpora.all():

            # Get a dozen random sentences from each corpus and put them in samples container
            corpus_samples.append([sentence.sentence for sentence in corpus.sentences.order_by('?')[:12]])
            # TODO: Make sure this update actually works, teehee


            Corpus.objects.filter(id=corpus.id).update(mash_count=F('mash_count') + 1)




        # Hard coded algo lookups based on choice field.. more algorithms will be added here and on the
        # mashup model as they are written
        if mashup.algorithm == 'MJN':
            # mouse_join expects two lists of sentences, snag a pair from our container or raise an error
            try:
                sent1, sent2 = random.sample(corpus_samples, 2)
            except:
                raise ValueError('The Mouse Join mashup algorithm needs at least two sources')

            # Cool stuff happens below :sunglasses: :100:

            try:
                # this algo returns a list, so join it
                mashed = " ".join(mashup_algorithms.mouse_join(sent1, sent2))
            except ValueError as e:
                raise ValueError(e)
                # Something went wrong...



        this_output = Output.objects.create(body=mashed, mashup=mashup)
        this_output.save()


    # success_url = reverse_lazy('output:output-detail')
    # display_url = '/view_output/{pk}/'.format(pk=outgoing.pk)

    # Relies on the get_absolute_url method on Output model
    return redirect(this_output)

class OutputListView(ListView):
    model = Output
    # TODO: Filter this to only show most recent or top or something like that
    def get_context_data(self, **kwargs):
        context = super(OutputListView, self).get_context_data(**kwargs)
        return context


class OutputDetailView(DetailView):
    model = Output
    context_object_name = 'Output'
    template_name = 'content/output_detail.html'



