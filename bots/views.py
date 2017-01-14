from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView

from .models import Bot
from .forms import BotForm


# from django.shortcuts import render

class BotDetailView(DetailView):
    """
    Conventional view for a single Bot
    """
    model = Bot
    context_object_name = 'bot'
    template_name = 'content/bot_detail.html'

class BotListViewByUser(ListView):
    model = Bot
    # TODO: Attach user to output
    context_object_name = 'bot_list'
    template_name = 'content/bot_list.html'
    # queryset = Output.objects.filter(output__id=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    # TODO: fix this.. passing queryset in to template
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user__id=self.kwargs['pk'])

class BotCreateView(CreateView):
    """
    Basic create view for defining a bot - oauth stuff happens separately
    """

    model = Bot
    template_name = 'content/create_bot.html'
    form_class = BotForm

    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        return super(BotCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('bot-detail', args=(self.object.id,))
