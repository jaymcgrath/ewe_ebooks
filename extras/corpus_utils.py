"""
Utilities for managing and maintaining individual Corpus objects
"""
from datetime import datetime, timedelta
from tzlocal import get_localzone
from .twittstopher import Timeline
from sources.models import Corpus, Sentence, Hashtag

# How long to wait before refreshing our timelines with new content?
DAYS_TIL_STALE = 1


def freshen_corpus(corpus):
    """
    Function for checking and updating stale twitter-based corpora
    :param corpus:
    :return:
    """
    local_tz = get_localzone()  # get local timezone
    now = datetime.now(local_tz)

    # Check to see if freshening is necessary

    if now - timedelta(days=DAYS_TIL_STALE) > corpus.updated:
        tl = Timeline(corpus.twitter_username, last_tweet_id=corpus.last_tweet_id)

        for sentence in tl.sentences:
            sent = Sentence.objects.create(corpus=corpus, sentence=sentence)
            sent.save()

        for hashtag in tl.hashtags:
            this_hash = Hashtag.objects.create(corpus=corpus, hashtag=hashtag)
            this_hash.save()

        # TODO: Uncomment after writing models that use each data type
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
        # for word in tl.words:
        #     wrd = Word.objects.create(corpus=self, word=word)
        #     wrd.save()

        corpus.last_tweet_id = tl.last_tweet_id
        corpus.save()



            # TODO: update corpus with fresh tweets and relateds -- break logic out of Corpus.save method?




