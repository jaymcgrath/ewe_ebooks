from django.contrib.auth.models import User
from django.db import models
from django.db.models import F

from bots.models import Bot
from extras import mashup_algorithms
from .managers import RandomManager

# Import the whole thing to avoid circular imports issues w extras.twittstopher and sources.models
from sources.models import Corpus

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
    corpora = models.ManyToManyField('sources.Corpus', related_name='mashups')
    algorithm = models.CharField(max_length=3, choices=ALGOS, default='MJN')
    created = models.DateTimeField(auto_now_add=True)
    public = models.BooleanField(default=False, help_text='Whether to display this mashup and its output publicly')
    created_by = models.ForeignKey(User, related_name='mashups')
    bot = models.ManyToManyField(Bot, related_name='mashups')

    # Add custom objects.random method for retrieving a random instance
    objects = RandomManager()

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
    sentences = models.ManyToManyField('sources.Sentence', related_name='outputs')


    def save(self, *args, **kwargs):
        """
        The get the mashup algo and sources, then do some munging and save it

        """
        if self.mashup.algorithm == 'MJN':
            # Randomly order the corpora we're going to join, this will generate better output
            mashed, parent_sents = mashup_algorithms.mouse_join(self.mashup.corpora.all(), smashtag=True)
        else:
            # TODO: add other join methods.. MJN used for everything rn
            mashed, parent_sents = mashup_algorithms.mouse_join(self.mashup.corpora.all(), smashtag=True)

        self.body = mashed

        super().save(*args, **kwargs)

        # Save the parent sentences.. M2M needs an instance first, so we add them after saving
        self.sentences.add(*parent_sents)

        # Update mash counts of the source corpora
        for corpus in self.mashup.corpora.all():

            Corpus.objects.filter(id=corpus.id).update(mash_count=F('mash_count') + 1)


    def __str__(self):  # __unicode__ on Python 2
        return "{m}: {b}.. {v}".format(m=self.mashup.title, b=self.body[:33], v=self.num_votes)

    def __repr__(self):
        return "{m}: {b}.. {v}".format(m=self.mashup.title, b=self.body[:33], v=self.num_votes)

    def get_absolute_url(self):
        return "/view_output/{pk}/".format(pk=self.id)
