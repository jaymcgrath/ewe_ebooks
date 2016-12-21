from django.db import models
from sources.models import Corpus
from django.contrib.auth.models import User


# Create your models here.
class MashupAlgorithm(models.Model):
    """
    Class of mashup methods and statistics about them
    (managed internally)
    """
    name = models.CharField(max_length=64)
    description = models.TextField()
    output_count = models.IntegerField(default=0)

    def __str__(self):  # __unicode__ on Python 2
        return self.name

    def __repr__(self):
        return self.name



class Mashup(models.Model):
    """
    Union of multiple sources.Corpus (corpora) and a MashupAlgorithm
    """
    ALGOS = (
        ('MJN', 'Mouse Join'),
        ('BOW', 'Bag of Words'),
        ('MDB', 'Mad Lib'),
    )

    title = models.CharField(max_length=32)
    description = models.TextField()
    corpora = models.ManyToManyField(Corpus, related_name='mashups')
    algorithm = models.CharField(max_length=3, choices=ALGOS, default='MJN')
    created = models.DateTimeField(auto_now=True)
    public = models.BooleanField(default=False, help_text='Whether to display this mashup and its output publicly')
    user = models.ForeignKey(User, related_name='mashups', default=1)


    def __str__(self):  # __unicode__ on Python 2
        return self.title

    def __repr__(self):
        return self.title


class Output(models.Model):
    """
    Instances of text generated by Mashups
    """
    body = models.CharField(max_length=144)
    generated = models.DateTimeField(auto_now=True)
    num_votes = models.PositiveIntegerField(default=0)
    mashup = models.ForeignKey(Mashup, related_name='outputs')

    def save(self, *args, **kwargs):
        """
        Get the mashup algorithm and sources, then do some munging and save it

        :param args:
        :param kwargs:
        :return:
        """

        super().save(*args, **kwargs)

    def __str__(self):  # __unicode__ on Python 2
        return "{m}: {b}.. {v}".format(m=self.mashup.title, b=self.body[:33], v=self.num_votes)

    def __repr__(self):
        return "{m}: {b}.. {v}".format(m=self.mashup.title, b=self.body[:33], v=self.num_votes)

    def get_absolute_url(self):
        return "/view_output/{pk}/".format(pk=self.id)

class Bot(models.Model):
    """
    Bot for posting mashups to twitter
    """
    name = models.CharField(max_length=64, help_text='A name for this bot (can be different from twitter username)')
    post_frequency = models.DurationField(null=True, default='12 hours', help_text='how frequently this bot posts')
    post_count = models.IntegerField(default=0)
    created = models.DateTimeField(auto_created=True, help_text='when this bot was created')
    updated = models.DateTimeField(auto_now=True, help_text='the last time this bot was updated')
    consumer_key = models.CharField(max_length=255, help_text='consumer key from dev.twitter.com')
    consumer_secret = models.CharField(max_length=255, help_text='consumer secret from dev.twitter.com ')
    access_token = models.CharField(max_length=255, help_text='access token from dev.twitter.com')
    access_token_secret = models.CharField(max_length=255, help_text='access token secret from dev.twitter.com')
    mashup = models.ForeignKey(Mashup, related_name='bots')
    user = models.ForeignKey(User, related_name='bots')


    def __str__(self):  # __unicode__ on Python 2
        return "{n}: {m} <{pf}>".format(n=self.name, m=self.mashup.title, pf=self.post_frequency)

    def __repr__(self):
        return "{n}: {m} <{pf}>".format(n=self.name, m=self.mashup.title, pf=self.post_frequency)

    def get_absolute_url(self):
        return "/view_bot/{pk}/".format(pk=self.id)









