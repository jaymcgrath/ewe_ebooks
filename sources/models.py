from django.contrib.auth.models import User
from django.db import models

from extras.bookstopher import Excerpt
from extras.twittstopher import Timeline, TwitterUser
from .managers import RandomManager


# Create your models here.


class Corpus(models.Model):
    """
    Meta representation of a linguistic source. Contains basic information but no body text. All actual
    content is stored in the other sources classes.
    """
    VARIETY_CHOICES = (
                    ("TW", "Twitter User"),
                    ("EX", "Text Excerpt"),
                    ("HS", "Twitter Hashtag"),
                    )

    title = models.CharField(max_length=64, help_text='The title for this source')
    body = models.TextField(null=True, help_text='Body of external corpora')
    added = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now=True)
    description = models.TextField(null=True, help_text='A description of this source')
    is_public = models.BooleanField(default=False)
    variety = models.CharField(max_length=2, choices=VARIETY_CHOICES, default='TW')
    twitter_username = models.CharField(max_length=15, unique=True, null=True)
    twitter_hashtag = models.CharField(max_length=140, unique=True, null=True)
    image_url = models.CharField(max_length=256, null=True)
    author = models.CharField(max_length=64, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    mash_count = models.BigIntegerField(default=0, editable=False)
    last_tweet_id = models.BigIntegerField(default=1, editable=False, help_text='id of most recent saved tweet')

    class Meta:
        verbose_name_plural = 'corpora'
        default_related_name = 'corpora'

    def __repr__(self):
        if self.variety == 'TW':
            return "{}: {}".format("Twitter: ", self.twitter_username)
        else:
            return "{}: {}".format("Excerpt: ", self.author)

    def __str__(self):
        if self.variety == 'TW':
            return "{}: {}".format("Twitter: ", self.twitter_username)
        else:
            return "{}: {}".format("Excerpt: ", self.author)

    def save(self, *args, **kwargs):
        """
        Fetch tweets and insert various aspects of Timeline object into database
        :param args:
        :param kwargs:
        :return:
        """

        if self.variety == 'TW':
            """
            Twitter Corpus - specific save method
            """

            if not self.pk:
                # If no PK exists for this object, it's new, so create it
                tweets_to_fetch = 50
                tl = Timeline(self.twitter_username, tweets_to_fetch)
                usr = TwitterUser(self.twitter_username)

                # TODO: fetch good values w Timeline class for author, description, title
                self.title = "Tweets of @{} aka {}".format(self.twitter_username, usr.name)
                self.description = usr.description
                self.variety = "TW"
                self.author = self.twitter_username
                self.image_url = usr.image
                self.last_tweet_id = tl.last_tweet_id
                self.twitter_hashtag = None

                super(Corpus, self).save(*args, **kwargs)

                """
                Ok, new corpus saved. Now process the dependencies..
                """
                # TODO: Uncomment after writing algorithms that use each data type
                # for word1, word2 in tl.bigrams:
                #     bg = Bigram.objects.create(corpus=self, word1=word1, word2=word2)
                #     bg.save()
                #
                # for word1, word2, word3 in tl.trigrams:
                #     tg = Trigram.objects.create(corpus=self, word1=word1, word2=word2, word3=word3)
                #     tg.save()
                #
                # for word1, word2, word3, word4 in tl.quadgrams:
                #     qg = Quadgram.objects.create(corpus=self, word1=word1, word2=word2, word3=word3, word4=word4)
                #     qg.save()

                for sentence in tl.sentences:
                    sent = Sentence.objects.create(corpus=self, sentence=sentence)
                    sent.save()

                for hashtag in tl.hashtags:
                    this_hash = Hashtag.objects.create(corpus=self, hashtag=hashtag)
                    this_hash.save()

                    # for word in tl.words:
                    #     wrd = Word.objects.create(corpus=self, word=word)
                    #     wrd.save()

            else:
                # Calling from corpus_utils.freshen_corpus, so just update instead
                super(Corpus, self).save(*args, **kwargs)

        elif self.variety == "EX":
            """
            Save method for external corpora
            """
            # For Null=True Unique field:
            self.twitter_hashtag = None
            self.twitter_username = None
            super(Corpus, self).save(*args, **kwargs)

            # Business logic is stored in bookstopher module
            ex = Excerpt(self.body)

            # Parse sentences with NLTK sentence Parser

            """
            Ok, new corpus saved. Now process the dependencies..
            """
            # TODO: Uncomment after writing algorithms that use each data type
            for word1, word2 in ex.bigrams:
                bg = Bigram.objects.create(corpus=self, word1=word1, word2=word2)
                bg.save()

            for word1, word2, word3 in ex.trigrams:
                tg = Trigram.objects.create(corpus=self, word1=word1, word2=word2, word3=word3)
                tg.save()

            for word1, word2, word3, word4 in ex.quadgrams:
                qg = Quadgram.objects.create(corpus=self, word1=word1, word2=word2, word3=word3, word4=word4)
                qg.save()

            for sentence in ex.sentences:
                sent = Sentence.objects.create(corpus=self, sentence=sentence)
                sent.save()

            for hashtag in ex.hashtags:
                this_hash = Hashtag.objects.create(corpus=self, hashtag=hashtag)
                this_hash.save()

            for word in ex.words:
                wrd = Word.objects.create(corpus=self, word=word)
                wrd.save()
        else:
            # Hashtag
            pass




class Word(models.Model):
    """
    contains words, each word relates back to a corpus..
    """
    word = models.CharField(max_length=32)
    corpus = models.ForeignKey(Corpus, related_name='words')

    #TODO: make this unique and store corpus: word counts in a separate M2M table?

    def __repr__(self):
        return "{a}: {w1}".format(a=self.corpus.author, w1=self.word)

    def __str__(self):
        return "{a}: {w1}".format(a=self.corpus.author, w1=self.word)




class Bigram(models.Model):
    """
    Word pairs from all corpora
    """
    word1 = models.CharField(max_length=32)
    word2 = models.CharField(max_length=32)
    corpus = models.ForeignKey(Corpus, related_name='bigrams')


    def __repr__(self):
        return "{a}: {w1} {w2}".format(a=self.corpus.author, w1=self.word1, w2=self.word2)

    def __str__(self):
        return "{a}: {w1} {w2}".format(a=self.corpus.author, w1=self.word1, w2=self.word2)


class Trigram(models.Model):
    """
    Word triplets from all corpora
    """
    word1 = models.CharField(max_length=32)
    word2 = models.CharField(max_length=32)
    word3 = models.CharField(max_length=32)
    corpus = models.ForeignKey(Corpus, related_name='trigrams')

    def __repr__(self):
        return "{a}: {w1} {w2} {w3}".format(a=self.corpus.author, w1=self.word1, w2=self.word2, w3=self.word3)

    def __str__(self):
        return "{a}: {w1} {w2} {w3}".format(a=self.corpus.author, w1=self.word1, w2=self.word2, w3=self.word3)

class Quadgram(models.Model):
    """
    Word quadruplets from all corpora
    """
    word1 = models.CharField(max_length=32)
    word2 = models.CharField(max_length=32)
    word3 = models.CharField(max_length=32)
    word4 = models.CharField(max_length=32)
    corpus = models.ForeignKey(Corpus, related_name='quadgrams')

    def __repr__(self):
        return "{a}: {w1} {w2} {w3} {w4}".format(a=self.corpus.author, w1=self.word1, w2=self.word2,
                                        w3=self.word3, w4=self.word4)

    def __str__(self):
        return "{a}: {w1} {w2} {w3} {w4}".format(a=self.corpus.author, w1=self.word1, w2=self.word2,
                                                 w3=self.word3, w4=self.word4)


class Sentence(models.Model):
    """
    Sentences from all corpora
    """
    # TODO: create custom tagged model for storing word:tag pairs as sentences
    sentence = models.TextField()
    corpus = models.ForeignKey(Corpus, related_name='sentences')

    objects = RandomManager()

    def __repr__(self):
        return "{}: {}".format(self.corpus.author, self.sentence[:42])

    def __str__(self):
        return "{}: {}".format(self.corpus.author, self.sentence[:42])


class Hashtag(models.Model):
    """
    Stores hashtags from all corpora
    """
    hashtag = models.CharField(max_length=64)
    corpus = models.ForeignKey(Corpus, related_name='hashtags')

    def __repr__(self):
        return "{}: #{}".format(self.corpus.author, self.hashtag)

    def __str__(self):
        return "{}: #{}".format(self.corpus.author, self.hashtag)
