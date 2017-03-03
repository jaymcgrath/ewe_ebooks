from django_cron import CronJobBase, Schedule

from extras.corpus_utils import freshen_corpus
from sources.models import Corpus


class RefreshCorpora(CronJobBase):
    """Scheduler for periodically refreshing twitter Corpora"""

    RUN_EVERY_MINS = 360  # every six hours

    schedule = Schedule(run_every_mins = RUN_EVERY_MINS)
    code = 'sources.refresh_corpora'    # a unique code

    def do(self):

        print("Examining Twitter Corpora...")
        # Get all the twitter Corpora
        corpus_queue = Corpus.objects.filter(variety__exact='TW')
        queue_len = len(corpus_queue)
        print("Created Corpus queue, length", queue_len)

        # Examine each one to check for freshness. Freshen if necessary
        for corpus in corpus_queue:
            try:
                print('examining', corpus.title)
                freshen_corpus(corpus)
            except:
                e = sys.exc_info()[0]
                print('Error', e)
