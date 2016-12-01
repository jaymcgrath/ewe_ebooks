from django.test import TestCase
from extras import twittstopher

class TestTimeline(TestCase):
    # Create timeline object from canonical twitter username
    tl = twittstopher.Timeline('jack', 500)

    def test_timeline_creation(self):
        self.assertIsInstance(self.tl, twittstopher.Timeline, 'Should instantiate a valid Timeline object')

    def test_has_bigrams(self):
        self.assertIsNotNone(self.tl.bigrams, 'Timeline object should contain at least one bigram')
