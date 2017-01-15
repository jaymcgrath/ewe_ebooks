import datetime

from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Bot(models.Model):
    """
    Bot for posting a mashups to twitter
    """

    # Note - Duration field takes a timedelta object
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
    user = models.ForeignKey(User, related_name='bots')


    def __str__(self):  # __unicode__ on Python 2
        return "{n}: postfreq: {pf} [{u}]".format(n=self.name, pf=self.post_frequency, u=self.user.username)

    def __repr__(self):
        return "{n}: postfreq: {pf} [{u}]".format(n=self.name, pf=self.post_frequency, u=self.user.username)

    def get_absolute_url(self):
      return "/view_bot/{pk}/".format(pk=self.id)