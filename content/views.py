from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.views.generic import ListView
from .forms import MashupForm
from .models import Mashup


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

