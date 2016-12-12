"""
Utilities for managing and maintaining individual Corpus objects
"""
from datetime import datetime, timedelta
from tzlocal import get_localzone
from .twittstopher import Timeline

# How long to wait before refreshing our timelines with new content?
DAYS_TIL_STALE = 1

from sources.models import Corpus

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
        freshened = Timeline(corpus.twitter_username, last_tweet_id=corpus.last_tweet_id)
        # TODO: update corpus with fresh tweets and relateds -- break logic out of Corpus.save method?


