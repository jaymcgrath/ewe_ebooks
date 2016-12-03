from django.db import models
from extras.twittstopher import Timeline

# Create your models here.

class Corpus(models.Model):
    """
    Meta representation of a linguistic source. Contains basic information but no body text. All actual
    content is stored in the other sources classes.
    """
    TYPE_CHOICES = (("TW", "Twitter"),
                    ("EX", "External")
                    )

    title = models.CharField(max_length=64, help_text="The title for this source")
    added = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now=True)
    desc = models.TextField(null=True, help_text="A description of this source")
    is_public = models.BooleanField(default=False)
    type = models.CharField(max_length=2, choices=TYPE_CHOICES)
    twitter_username = models.CharField(max_length=15, null=True)
    author = models.TextField(max_length=64, null=True)
    # TODO: remove default=1 from added_by to link it with people.Member
    added_by = models.ForeignKey('people.Member', on_delete=models.CASCADE, default=1)
    mash_count = models.IntegerField(default=0, editable=False)

    class Meta:
        verbose_name_plural = 'corpora'
        default_related_name = 'corpora'

    def __repr__(self):
        return self.title

    def save(self, *args, **kwargs):
        """
        Fetch tweets and insert various aspects of Timeline object into database
        :param args:
        :param kwargs:
        :return:
        """

        tl = Timeline(self.twitter_username)
        # TODO: fetch good values w Timeline class for author, desc, title
        self.title = "Twitter timeline of {}".format(self.twitter_username)
        self.desc = "The collected wisdom of {}".format(self.twitter_username)
        self.type = "TW"
        self.author = self.twitter_username

        super(Corpus, self).save(*args, **kwargs)

        for word1, word2 in tl.bigrams:
            bg = Bigram.objects.create(corpus=self, word1=word1, word2=word2)
            bg.save()

        for word1, word2, word3 in tl.trigrams:
            tg = Trigram.objects.create(corpus=self, word1=word1, word2=word2, word3=word3)
            tg.save()

        for word1, word2, word3, word4 in tl.quadgrams:
            qg = Quadgram.objects.create(corpus=self, word1=word1, word2=word2, word3=word3, word4=word4)
            qg.save()

        for sentence in tl.sentences:
            sent = Sentence.objects.create(corpus=self, sentence=sentence)
            sent.save()

        for word in tl.words:
            wrd = Word.objects.create(corpus=self, word=word)
            wrd.save()


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
    sentence = models.CharField(max_length=1024)
    corpus = models.ForeignKey(Corpus)


class Hashtag(models.Model):
    """
    Stores hashtags from all corpora
    """
    hashtag = models.CharField(max_length=64)
    corpus = models.ForeignKey(Corpus)
