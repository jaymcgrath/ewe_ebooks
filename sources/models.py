from django.db import models

# Create your models here.

class Corpus(models.Model):
    """
    Meta representation of a linguistic source. Contains basic information but no body text. All actual
    content is stored in the other sources classes.
    """
    TYPE_CHOICES = [
                    "Twitter",
                    "External"
    ]

    title = models.CharField(max_length=64, help_text="The title for this source")
    added = models.DateTimeField(auto_created=True)
    updated = models.DateTimeField()
    desc = models.TextField(null=True, help_text = "A description of this source")
    is_public = models.BooleanField(default=False)
    type = models.CharField(max_lenth=8, choices=TYPE_CHOICES)
    twitter_username = models.CharField(max_length=15, null)
    author = models.TextField(max_length=64, null=True)
    added_by = models.ForeignKey(Member, on_delete=models.CASCADE)
    mash_count = models.IntegerField(default=0)

class Word(models.Model):
    """
    contains words, each word relates back to a corpus..
    TODO: make this unique and store corpus: word counts in a separate M2M table?
    """
    word = models.CharField(max_length=32)
    corpus = models.ForeignKey(Corpus)

class Bigram(models.Model):
    """
    Word pairs from all corpora
    """
    word1 = models.CharField(max_length=32)
    word2 = models.CharField(max_length=32)
    corpus = models.ForeignKey(Corpus)

class Trigram(models.Model):
    """
    Word triplets from all corpora
    """
    word1 = models.CharField(max_length=32)
    word2 = models.CharField(max_length=32)
    word3 = models.CharField(max_length=32)
    corpus = models.ForeignKey(Corpus)

class Quadgram(models.Model):
    """
    Word quadruplets from all corpora
    """
    word1 = models.CharField(max_length=32)
    word2 = models.CharField(max_length=32)
    word3 = models.CharField(max_length=32)
    word4 = models.CharField(max_length=32)
    corpus = models.ForeignKey(Corpus)

class Sentence(models.Model):
    """
    Sentences from all corpora
    """
    # TODO: create custom tagged model for storing word:tag pairs as sentences
    sentence = models.CharField()
    corpus = models.ForeignKey(Corpus)

class Hashtag:
    """
    Stores hashtags from all corpora
    """
    hashtag = models.CharField(max_length=64)
    corpus = models.ForeignKey(Corpus)

