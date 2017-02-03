from datetime import datetime, timezone, timedelta

from django_cron import CronJobBase, Schedule

from sources.models import Corpus
from .corpus_utils import freshen_corpus


DAYS_TIL_STALE = 1
# RUN_EVERY_MINS = 720 # every 12 hours
RUN_EVERY_MINS = 1  # Test setting


class RefreshCorpora(CronJobBase):
    """Scheduler for periodically checking and freshening stale twitter corpora"""

    schedule = Schedule(run_every_mins = RUN_EVERY_MINS)
    code = 'sources.refresh_corpora'    # a unique code

    def do(self):
        # Get expiration date for the timeline
        fresh_until = datetime.now(timezone.utc) - timedelta(days=DAYS_TIL_STALE)
        # Retrieve corpora updated less recently than the expiration
        corpus_queue = Corpus.objects.filter(updated__lt=fresh_until).filter(variety__exact='TW')

        # Examine all the bots and tweet if they are overdue
        for this_corpus in corpus_queue:
            print("checking born-on date for", this_corpus)
            freshen_corpus(this_corpus)