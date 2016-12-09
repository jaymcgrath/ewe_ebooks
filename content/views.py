import random

from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from django.db.models import F

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, mixins, generics

from .forms import MashupForm
from .models import Mashup, Output
from sources.models import Corpus

from .serializers import OutputSerializer, OutputWriteSerializer

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
    queryset = Mashup.objects.order_by('-created')
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

        # Hard coded algo lookups based on choice field.. more algorithms will be added here and on the
        # mashup model as they are written

        if mashup.algorithm == 'MJN':
            # Randomly order the corpora we're going to join, this will generate better output
            mashed = mashup_algorithms.mouse_join(mashup.corpora.all().order_by('?'), smashtag=True)

            # # Get the related corpora for this mashup, then select a random sentence from each
            #
            # # Create container for random slices of sentences
            # corpus_samples = list()
            #
            # for corpus in :
            #     """
            #     Get up to a dozen random sentences and hashtags from each corpus and
            #     store them as tuples in our corpus_samples container
            #     data structure: list of these tuples, ([sentences, ], [hashtags, ])
            #     """
            #     corpus_samples.append(
            #         (
            #         [sentence.sentence for sentence in corpus.sentences.order_by('?')[:12]],
            #         [hashtag.hashtag for hashtag in corpus.hashtags.all().order_by('?')[:24]],
            #         )
            #     )
            #     # TODO: Make sure this update actually works, teehee
            #
            #     # Increment mash_count for this corpus
            #     Corpus.objects.filter(id=corpus.id).update(mash_count=F('mash_count') + 1)
            #
            # # mouse_join expects two lists of sentences, snag a pair from our container or raise an error
            # try:
            #     samp1, samp2 = random.sample(corpus_samples, 2)
            # except:
            #     raise ValueError('The Mouse Join mashup algorithm needs at least two sources')
            #
            # # Cool stuff happens below :sunglasses: :100:
            #
            # try:
            #     # this algo returns a list of words, concatenate them into a sentence
            #     mashed = " ".join(mashup_algorithms.mouse_join(samp1[0], samp2[0]))
            #
            #     #TODO: try to make a smashtag - random conjoined hashtag
            #     if len(samp1[1])> 0 and len(samp2[1]) > 0:
            #         smashtag = '#' + ''.join((random.choice(samp1[1]), random.choice(samp2[1]),))
            #         mashed += " " + smashtag
            #
            #
            #
            #
            # except ValueError as e:
            #     raise ValueError(e)
            #     # Something went wrong...
            #
            #

        this_output = Output.objects.create(body=mashed, mashup=mashup)
        this_output.save()


    # Relies on the get_absolute_url method on Output model
    return redirect(this_output)


class OutputListView(ListView):
    model = Output
    # TODO: Filter this to only show most recent or top or something like that
    context_object_name = 'output_list'
    template_name = 'content/output_list.html'
    def get_context_data(self, **kwargs):
        context = super(OutputListView, self).get_context_data(**kwargs)
        return context


class OutputDetailView(DetailView):
    """
    Conventional view for Output
    """
    model = Output
    context_object_name = 'output'
    template_name = 'content/output_detail.html'

class CreateOutputView(generics.ListCreateAPIView):
    pass
    # TODO: create this view

class DisplayOutputView(generics.RetrieveUpdateDestroyAPIView):
    """
    RESTful API view for getting/
    """
    queryset = Output.objects.all()
    serializer_class = OutputSerializer
    # TODO: create this view





