from datetime import datetime, timezone

from django_cron import CronJobBase, Schedule

from bots.models import Bot, Tweet
from content.models import Output


class GenerateTweets(CronJobBase):
    """Scheduler for periodically tweeting for overdue bots"""

    RUN_EVERY_MINS = 30 # every half hour

    schedule = Schedule(run_every_mins = RUN_EVERY_MINS)
    code = 'bots.generate_tweets'    # a unique code

    def do(self):
        # Get all the bots in a queryset
        bot_queue = Bot.objects.all()

        # Examine all the bots and tweet if they are overdue
        for this_bot in bot_queue:

            # Check if last update + how frequently they post is less than now, if so, fire a tweet
            if bot.post_frequency + bot.updated < datetime.now(timezone.utc) and bot.is_active == True:
                print("overdue:", this_bot.name)

                # Bots can have multiple mashups, so select one at random
                this_mashup = this_bot.mashup.random()

                # Now, we just make an output, attach all the stuff to a Tweet instance, and save it

                this_output = Output(mashup=this_mashup)
                this_output.save()

                this_tweet = Tweet(bot=this_bot, output=this_output, mashup=this_mashup)
                this_tweet.save()