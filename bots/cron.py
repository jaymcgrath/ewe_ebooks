from datetime import datetime, timezone

from django_cron import CronJobBase, Schedule

from bots.models import Bot, Tweet


class GenerateTweets(CronJobBase):
    """Scheduler for periodically tweeting for overdue bots"""

    RUN_EVERY_MINS = 1 # every 2 mins

    schedule = Schedule(run_every_mins = RUN_EVERY_MINS)
    code = 'bots.generate_tweets'    # a unique code

    def do(self):
        print("queueing bots")
        bot_queue = Bot.objects.all()

        # Examine all the bots
        for bot in bot_queue:
            print("examining", bot.name)
            # Check if last update + how frequently they post is less than now, if so, fire a tweet
            if bot.post_frequency + bot.updated < datetime.now(timezone.utc) and bot.is_active == True:
                print("overdue:", bot.name)
                new_tweet = Tweet(bot=bot)

                # Pretty much all the business is on the save() method of Tweet Model
                new_tweet.save()
