from django.contrib.auth.models import User
from django.db import models

from bots.models import Bot
from sources.models import Corpus, Sentence


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
    created = models.DateTimeField(auto_now_add=True)
    public = models.BooleanField(default=False, help_text='Whether to display this mashup and its output publicly')
    user = models.ForeignKey(User, related_name='mashups', default=1)
    bot = models.ManyToManyField(Bot, related_name='mashups')

    def __str__(self):  # __unicode__ on Python 2
        return self.title

    def __repr__(self):
        return self.title


class Output(models.Model):
    """
    Instances of text generated by Mashups
    """
    body = models.TextField()
    generated = models.DateTimeField(auto_now_add=True)
    num_votes = models.PositiveIntegerField(default=0)
    mashup = models.ForeignKey(Mashup, related_name='outputs')
    sentences = models.ManyToManyField(Sentence, related_name='outputs')


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
