from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView

from .models import Bot
from .forms import BotForm

import urllib.parse
import oauth2 as oauth
import os

# from django.shortcuts import render

CONSUMER_KEY = os.environ['CONSUMER_KEY']
CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']


class BotDetailView(DetailView):
    """
    Conventional view for a single Bot
    """
    model = Bot
    context_object_name = 'bot'
    template_name = 'bots/bot_detail.html'

class BotListViewByUser(ListView):
    model = Bot
    # TODO: Attach user to output
    context_object_name = 'bot_list'
    template_name = 'bots/bot_list.html'
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

class BotAuthorizeView(DetailView):
    """
    view for three-legged oauth key retrieval to allow ewe_ebooks to post on user's behalf
    """
    model = Bot
    context_object_name = 'bot'
    template_name = 'bots/bot_authorize.html'

    # TODO: check GET dict for the following vars: oauth_token auth_verifier - if exist, write to db and redirect back to bot view

    def get_bot_auth_url(self):
        """
        Function for generating three-legged oauth url -
        writes temporary keys to bot.request instance for retrieval by the callback func

        """

        request_token_url = 'https://api.twitter.com/oauth/request_token'
        access_token_url = 'https://api.twitter.com/oauth/access_token'
        authorize_url = 'https://api.twitter.com/oauth/authorize'
        # TODO : implement request.build_absolute_uri(reverse('view_name', args=(obj.pk, ))) below for more portability
        callback_url = 'http://127.0.0.1:8000/authorize_bot/{}/'.format(self.kwargs['pk'])
        consumer = oauth.Consumer(CONSUMER_KEY, CONSUMER_SECRET)
        client = oauth.Client(consumer)
        resp, content = client.request(request_token_url, "POST",
                                       body=urllib.parse.urlencode({'oauth_callback':callback_url}))

        if resp['status'] != '200':
            raise Exception("Invalid response %s." % resp['status'])

        request_token = dict(urllib.parse.parse_qsl(content))

        # urllib returns bytes, which will need to be decoded using the string.decode() method before use
        request_token = {key.decode(): value.decode() for key, value in request_token.items()}

        return("{}?oauth_token={}".format(authorize_url, request_token['oauth_token']))

    # Add the authorization url to the context so we can present it to the user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bot_auth_url = self.get_bot_auth_url()
        context.update({'bot_auth_url': bot_auth_url})
        return context











