import random

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from rest_framework import generics

from api.serializers import OutputSerializer
from extras import mashup_algorithms
from sources.models import Corpus
from .forms import MashupForm
from .models import Mashup, Output


class MashupCreateView(LoginRequiredMixin, CreateView):
    """
    Class view for adding a mashup.
    """

    template_name = 'content/create_mashup.html'
    form_class = MashupForm
    success_url = '/list_mashups/'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super(MashupCreateView, self).form_valid(form)


class MashupListView(ListView):
    """
    Generic mashup list available to everyone
    """

    model = Mashup
    queryset = Mashup.objects.order_by('-created')

    def get_context_data(self, **kwargs):
        context = super(MashupListView, self).get_context_data(**kwargs)
        return context


class MashupUserListView(LoginRequiredMixin, MashupListView):
    """
    Mashup list view filtered by logged in user.. subclasses MashupListView
    """

    def get_context_data(self, **kwargs):
        context = super(MashupListView, self).get_context_data(**kwargs)
        return context

    def get_queryset(self, **kwargs):
        # Filter these mashups by the currently logged in user
        qs = Mashup.objects.filter(created_by=self.request.user)

        return qs


class MashupDetailView(DetailView):
    model = Mashup
    context_object_name = 'mashup'
    template_name = 'content/mashup_detail.html'


@login_required
def OutputCreateView(request):
    """
    FBV for making content from a mashup
    """
    if request.method == 'POST':
        # mashup_id is passed in as a hidden form field
        mashup = Mashup.objects.get(id=request.POST['mashup_id'])

        # Business logic is in Output.save
        this_output = Output(mashup=mashup)
        this_output.save()

    return redirect(this_output)


@login_required
def OutputRandomView(request):
    """
    Endpoint for generating output from 2 randomly selected corpora
    Optional save button on display
    :param request:
    :return:
    """

    # TODO: select random join method as well

    """
    Avoid expensive random database ordering and just grab 2 random queryset indices
    If a new corpus is created between counting this queryset and selecting against it,
    the new corpus won't be eligible to appear, but that is officially No Big Deal
    """

    last = Corpus.objects.count() - 1

    randidx1 = random.randint(0, last)
    randidx2 = random.randint(0, last - 1)

    if randidx1 == randidx2:
        # Just make sure they aren't the same
        randidx2 = last

    rand_corpora = [Corpus.objects.all()[randidx1], Corpus.objects.all()[randidx2]]

    """
    Check if there's already a mashup with just these two corpora, if so, load it,
    otherwise, create it
    """
    id1, id2 = [corpus.id for corpus in rand_corpora]

    # Try to find a mashup that already has these two corpora as sources:

    if Mashup.objects.filter(corpora__id=id1).filter(corpora__id=id2).exists():
        # We got at least one match. Attribute this tweet to that source
        mashup = Mashup.objects.filter(corpora__id=id1).filter(corpora__id=id2)[0]

    else:  # Create this mashup on the fly
        corpus1, corpus2 = rand_corpora
        mashup_details = {
            'title': "{} vs. {} (rando)".format(corpus1.twitter_username, corpus2.twitter_username),
            'description': "randomly created, new mashup from /random/",
            'algorithm': 'MJN', #TODO: select this randomly too
            'public': True
            }


        mashup = Mashup(**mashup_details)
        mashup.save()
        # Have to save it before adding a M2M relationship
        mashup.corpora.add(*rand_corpora)
        mashup.save()

    if mashup.algorithm == 'MJN':
        # Randomly order the corpora we're going to join, this will generate better output
        mashed = mashup_algorithms.mouse_join(mashup.corpora.all().order_by('?'), smashtag=True)

    this_output = Output.objects.create(body=mashed, mashup=mashup)
    this_output.save()

    # Update mash_counts for the various corpora just used:
    for corpus in mashup.corpora.all():
        Corpus.objects.filter(id=corpus.id).update(mash_count=F('mash_count') + 1)

    return redirect(this_output)

class OutputListView(ListView):
    model = Output
    # TODO: Filter this to only show most recent or top or something like that
    context_object_name = 'output_list'
    template_name = 'content/output_list.html'
    def get_context_data(self, **kwargs):
        context = super(OutputListView, self).get_context_data(**kwargs)
        return context


class OutputUserListView(ListView):
    model = Output
    # TODO: Attach user to output
    context_object_name = 'output_list'
    template_name = 'content/output_list.html'
    # queryset = Output.objects.filter(output__id=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    # TODO: fix this.. get outputs filtered by mashup filtered by user

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(mashup__created_by__id=self.kwargs['pk'])


class OutputDetailView(DetailView):
    """
    Conventional view for Output
    """
    model = Output
    context_object_name = 'output'
    template_name = 'content/output_detail.html'


#TODO: move to api app

class DisplayOutputView(generics.RetrieveUpdateDestroyAPIView):
    """
    RESTful API view for getting/
    """
    queryset = Output.objects.all()
    serializer_class = OutputSerializer
    # TODO: create this view
