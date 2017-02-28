from datetime import datetime, timezone

from django_cron import CronJobBase, Schedule

from bots.models import Bot, Tweet
from content.models import Output

import os

import logging
import tweepy

# Fetch ewe_ebooks twitter API keys
CONSUMER_KEY = os.environ['CONSUMER_KEY']
CONSUMER_SECRET = os.environ['CONSUMER_SECRET']


class GenerateTweets(CronJobBase):
    """Scheduler for periodically tweeting for overdue bots"""

    RUN_EVERY_MINS = 1  # every half hour

    schedule = Schedule(run_every_mins = RUN_EVERY_MINS)
    code = 'bots.generate_tweets'    # a unique code

    def do(self):
        # Get all the bots in a queryset
        bot_queue = Bot.objects.all()
        # Examine all the bots and tweet if they are overdue
        for this_bot in bot_queue:
            # Check if last update + how frequently they post is less than now, if so, fire a tweet
            if this_bot.post_frequency + this_bot.updated < datetime.now(timezone.utc) and this_bot.is_active == True:

                # Bots can have multiple mashups, so select one at random
                this_mashup = this_bot.mashup.random()

                # Now, we just make an output, attach all the stuff to a Tweet instance, and save it

                this_output = Output(mashup=this_mashup)
                this_output.save()

                this_tweet = Tweet(bot=this_bot, output=this_output, mashup=this_mashup)
                this_tweet.save()

                try:
                    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
                    assert(this_bot.access_token and this_bot.access_token_secret)
                    auth.set_access_token(this_bot.access_token, this_bot.access_token_secret)

                    api = tweepy.API(auth)
                    status = api.update_status(status=this_output.body)
                    this_tweet.tweet_id = status.id
                    this_tweet.created_twitter = status.created_at
                    this_tweet.text = status.text
                    this_tweet.screen_name = status.user.screen_name

                    this_tweet.save()


                    # Retreive details of tweet and write to Tweet object

                except (AssertionError, ValueError, tweepy.TweepError) as e:
                    # Get an instance of a logger
                    logger = logging.getLogger(__name__)
                    err_template = 'Error posting from {bot}: {err}'
                    logger.error(err_template.format(bot=this_bot.name, err=e))






