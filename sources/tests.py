from django.test import TestCase
from mixer.backend.django import mixer
from extras import twittstopher


# Create your tests here.

class TestCorpus(TestCase):
    tl = twittstopher.Timeline('jack', 500)
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_has_bigrams(self):
        pass

    def test_corpus_model_instanation(self):
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

