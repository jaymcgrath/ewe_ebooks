import pickle
from django.test import TestCase

# Create timeline object from canonical source

with open('timeline_fixture.p', 'rb')as tl_fixture:
    tl = pickle.load(tl_fixture)

# Create your tests here.

class TestCorpus(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_has_bigrams(self):
        assert(tl.bigrams is not Null)

    def test_corpus_database_insertion(self):
        pass

class TestBigram(TestCase):
    pass

class TestTrigram(TestCase):
    pass

class TestQuadgram(TestCase):
    pass

class TestSentence(TestCase):
    pass

class TestWord(TestCase):
    pass

