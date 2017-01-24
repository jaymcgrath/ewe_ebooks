from django.urls import reverse
from django.views.generic import ListView, DetailView, View, UpdateView
from django.views.generic.edit import CreateView
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Bot, Tweet
from content.models import Output
from .forms import BotForm

import urllib.parse
import oauth2 as oauth
import os

# from django.shortcuts import render

CONSUMER_KEY = os.environ['CONSUMER_KEY']
CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']


class BotDetailView(LoginRequiredMixin, DetailView):
    """
    Conventional view for a single Bot
    """
    model = Bot
    context_object_name = 'bot'
    template_name = 'bots/bot_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        return context

class BotListViewByUser(LoginRequiredMixin, ListView):
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
        return qs.filter(created_by__id=self.kwargs['pk'])

class BotCreateView(LoginRequiredMixin, CreateView):
    """
    Basic create view for defining a bot - oauth stuff happens separately
    """

    model = Bot
    template_name = 'bots/create_bot.html'
    form_class = BotForm

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super(BotCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('bot-detail', args=(self.object.id,))

class BotEditView(LoginRequiredMixin, UpdateView):
    """
    View for updating parts of a bot
    """
    model = Bot
    template_name = 'bots/bot_edit.html'
    form_class = BotForm

    def get_success_url(self):
        return reverse('bot-detail', args=(self.object.id,))

class BotAuthorizeView(LoginRequiredMixin, DetailView):
    """
    view for three-legged oauth key retrieval to allow ewe_ebooks to post on user's behalf
    """
    model = Bot
    context_object_name = 'bot'
    template_name = 'bots/bot_authorize.html'

    # Vars for oauth dance
    REQUEST_TOKEN_URL = 'https://api.twitter.com/oauth/request_token'
    ACCESS_TOKEN_URL = 'https://api.twitter.com/oauth/access_token'
    AUTHORIZE_URL = 'https://api.twitter.com/oauth/authorize'



    def get(self, request, *args, **kwargs):
        """
        Overwrite the default get method for this view so we can use the same view for both parts of the
         authorization process
        """
        self.object = self.get_object()

        # Set token values to empty str if they're not there
        oauth_token = request.GET.get('oauth_token', '')
        oauth_verifier = request.GET.get('oauth_verifier', '')


        # Check if this is a callback from twitter authorization with the tokens:
        if oauth_token and oauth_verifier:
            """
            Ok, this is an oauth_callback from twitter, we have both vars in the GET env
             extract them and compare to the values in our DB, then generate and store a permanent token pair
            """
            request_token = self.object.request_token

            if oauth_token != request_token:
                # Note - these tokens are temporary throwaways, so exposing them in an exception msg here is OK
                error_msg = "Error, oauth_token {} and request_token {} do not match".format(oauth_token, request_token)
                raise Exception(error_msg)

            oauth_token_secret = self.object.request_token_secret

            access_token = self.get_access_token(oauth_token, oauth_token_secret, oauth_verifier)

            self.object.access_token = access_token['oauth_token']
            self.object.access_token_secret = access_token['oauth_token_secret']
            self.object.save()

            # All saved and ready to roll. Redirect to bot detail page
            return redirect('bot-detail', pk=self.object.pk)

        # OK, not a callback.. generate an oauth authorize url via get_context_data method
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


    def get_request_token(self):
        """
        Function for generating initial request token for three-legged oauth
        Takes no input, returns a request_token dict with two keys, oauth_token and oauth_token_secret
        """

        # TODO : implement request.build_absolute_uri(reverse('view_name', args=(obj.pk, ))) below for more portability
        callback_url = 'http://127.0.0.1:8000/authorize_bot/{}/'.format(self.object.pk)

        consumer = oauth.Consumer(CONSUMER_KEY, CONSUMER_SECRET)
        client = oauth.Client(consumer)
        resp, content = client.request(self.REQUEST_TOKEN_URL, "POST",
                                       body=urllib.parse.urlencode({'oauth_callback':callback_url}))

        if resp['status'] != '200':
            raise Exception("Invalid response %s." % resp['status'])

        request_token = dict(urllib.parse.parse_qsl(content))

        # urllib returns bytes, which will need to be decoded using the string.decode() method before use
        request_token = {key.decode(): value.decode() for key, value in request_token.items()}

        # Return the token dict containing token and secret
        return(request_token)

    def get_access_token(self, oauth_token, oauth_token_secret, oauth_verifier):
        """
        Func for final leg of three-legged oauth,
        takes token and secret returned in oauth_callback GET dict and
         exchanges them for the permanent access token and secret
        returns an access_token dict with two keys, oauth_token and oauth_token_secret
        """
        token = oauth.Token(oauth_token, oauth_token_secret)
        token.set_verifier(oauth_verifier)
        consumer = oauth.Consumer(CONSUMER_KEY, CONSUMER_SECRET)
        client = oauth.Client(consumer, token)

        # Now we fire the request at access token url instead of request token
        resp, content = client.request(self.ACCESS_TOKEN_URL, "POST")

        if resp['status'] != '200':
            raise Exception("Invalid response %s." % resp['status'])

        access_token = dict(urllib.parse.parse_qsl(content))

        # urllib returns bytes, which will need to be decoded using the string.decode() method before use
        access_token = {key.decode(): value.decode() for key, value in access_token.items()}

        # Return the token dict containing token and secret
        return (access_token)




    def get_context_data(self, **kwargs):
        """
        Add the authorization url to the context so we can link it in the template
        save the request token data to model for later comparison
        """

        context = super().get_context_data(**kwargs)

        # Generate temporary auth tokens
        request_token = self.get_request_token()

        # Retrieve our model instance
        this_bot = self.get_object()

        # Update and save tokens to db for later comparison
        this_bot.request_token = request_token['oauth_token']
        this_bot.request_token_secret = request_token['oauth_token_secret']
        this_bot.save()

        # Format url with the request token and add it to the context
        bot_auth_url = "{}?oauth_token={}".format(self.AUTHORIZE_URL, request_token['oauth_token'])
        context.update({'bot_auth_url': bot_auth_url})
        return context


class TweetCreateView(LoginRequiredMixin, View):
    """
    Custom View for creating a tweet with a fully configured bot
    """

    def get(self, *args, **kwargs):

        # Bot ID should have come in as a pk
        this_bot = Bot.objects.get(id=self.kwargs['pk'])

        # Bots can have multiple mashups, so select one at random
        this_mashup = this_bot.mashup.random()

        # Now, we just make an output, attach all the stuff to a Tweet instance, and save it

        this_output = Output(mashup=this_mashup)
        this_output.save()


        this_tweet = Tweet(bot=this_bot, output=this_output, mashup=this_mashup)
        this_tweet.save()



        # OK, redirect to view what we just posted
        return redirect(reverse('tweet-detail', args=(this_tweet.pk,)))


class TweetDetailView(DetailView):
    """
    Basic view for displaying a single tweet
    """
    model = Tweet
    context_object_name = 'tweet'
    template_name = 'bots/tweet_detail.html'









