import datetime
import os

import tweepy
from django.contrib.auth.models import User
from django.db import models


CONSUMER_KEY = os.environ['CONSUMER_KEY']
CONSUMER_SECRET = os.environ['CONSUMER_SECRET']

class Bot(models.Model):
    """
    Bot for posting a mashups to twitter
    """

    # Note - post_frequency is a duration field that takes a timedelta object
    POST_FREQS = (
                (datetime.timedelta(hours=6), 'Four times daily'),
                (datetime.timedelta(hours=12), 'Twice daily'),
                (datetime.timedelta(days=1), 'Once Daily'),
                (datetime.timedelta(days=2), 'Every Other Day'),
    )
    name = models.CharField(max_length=64, help_text='A name for this bot (can be different from twitter username)')
    description = models.TextField(null=True, help_text='A brief description of how this bot looks on Twitter')
    post_frequency = models.DurationField(null=True, choices=POST_FREQS, default='12 hours',
                                          help_text='how frequently this bot posts')
    post_count = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True, help_text='when this bot was created')
    updated = models.DateTimeField(auto_now=True, help_text='the last time this bot was updated')
    request_token = models.CharField(max_length=255, null=True, blank=True, help_text='temporary key from oauth')
    request_token_secret = models.CharField(max_length=255, null=True, blank=True, help_text='temporary key from oauth')
    access_token = models.CharField(max_length=255, null=True, blank=True,
                                    help_text='permanent access token for posting to twitter')
    access_token_secret = models.CharField(max_length=255, null=True, blank=True,
                                           help_text='permanent access token secret for posting to twitter')
    mashup = models.ManyToManyField('content.Mashup', related_name='bots')
    created_by = models.ForeignKey(User, related_name='bots')

    def __str__(self):  # __unicode__ on Python 2
        return "{n}: postfreq: {pf} [{u}]".format(n=self.name, pf=self.post_frequency, u=self.created_by.username)

    def __repr__(self):
        return "{n}: postfreq: {pf} [{u}]".format(n=self.name, pf=self.post_frequency, u=self.created_by.username)

    def get_absolute_url(self):
      return "/view_bot/{pk}/".format(pk=self.id)

class Tweet(models.Model):
    """
    Model for logging Mashup Output posted to twitter by Bots
    """

    tweet_id = models.BigIntegerField(help_text='twitter status ID of this tweet')
    created = models.DateTimeField(auto_now_add=True, help_text='local timestamp')
    created_twitter = models.DateTimeField(null=True, help_text='twitter creation timestamp')
    bot = models.ForeignKey(Bot, related_name='tweets')
    mashup = models.ForeignKey('content.Mashup', related_name='tweets', help_text='the mashup used in creation')
    output = models.ForeignKey('content.Output', related_name='tweets', help_text='the output object posted to twitter')
    text = models.CharField(max_length=157, help_text='the actual body of the tweet as posted on twitter')
    retweet_count = models.IntegerField(default=0, help_text='the number of retweets this tweet has received')
    screen_name = models.CharField(max_length=16, help_text='screen_name of the account that posted this')

    def __str__(self):
        return "<{b}>{t}".format(b=self.bot.name, t=self.text)

    def __repr__(self):
        return "<{b}>{t}".format(b=self.bot.name, t=self.text)

    def get_absolute_url(self):
      return "/view_tweet/{pk}/".format(pk=self.id)

    def save(self, *args, **kwargs):
        """
        attempt to generate an output instance and post it to twitter, log result

        :param args:
        :param kwargs:
        :return:
        """
        if not self.pk:
            # Only post to twitter when creating a new object
            auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
            auth.set_access_token(self.bot.access_token, self.bot.access_token_secret)
            api = tweepy.API(auth)

            # Post to twitter and record details to a status object
            # Gotta just truncate it at 140
            this_tweet = api.update_status(self.output.body[:140])

            # Assign relevant details to our object
            self.tweet_id = this_tweet.id
            self.created_twitter = this_tweet.created_at
            self.text = this_tweet.text

            # This is the twitter user from the tweepy api that just posted the tweet, not a django user object
            self.screen_name = this_tweet.user.screen_name

        # Either way, save it

        super().save(*args, **kwargs)



