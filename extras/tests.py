import pickle
from django.test import TestCase
from extras import twittstopher
import pytest

# Create timeline object from canonical source
pytestmark = pytest.mark.django_db

with open('timeline_fixture.p', 'rb')as tl_fixture:
    tl = pickle.load(tl_fixture)


class TestTimeline(TestCase):

    def test_timeline_creation(self):
        self.assertIsInstance(self.tl, twittstopher.Timeline, 'Should instantiate a valid Timeline object')

    def test_has_bigrams(self):
        self.assertIsNotNone(self.tl.bigrams, 'Timeline object should contain at least one bigram')

    def test_has_trigrams(self):
        self.assertIsNotNone(self.tl.trigrams, 'Timeline object should contain at least one trigram')

    def test_has_quadgrams(self):
        self.assertIsNotNone(self.tl.quadgrams, 'Timeline object should contain at least one quadgram')

    def test_has_sentences(self):
        self.assertIsNotNone(self.tl.sentences, 'Timeline object should contain at least one sentence')

    def test_has_words(self):
        self.assertIsNotNone(self.tl.words, 'Timeline object should contain at least one word')




