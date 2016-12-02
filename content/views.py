from django.shortcuts import render
from django.views.generic.edit import CreateView

from .forms import MashupForm


# Create your views here.
class CreateMashupView(CreateView):
    template_name = 'create_mashup.html'
    form_class = MashupForm
    success_url = '/view_mashups/'

