from unittest.mock import patch

import pytest
from django.test import TestCase
from mixer.backend.django import mixer

from sources import models

pytestmark = pytest.mark.django_db

class TimelineFixture:
    """ Mock Timeline fixture for API testing """

    words = [
                'You',
                'want',
                'something',
                'memorable',
                'and',
                'weird',
                ',',
                'go',
                'check',
                'out',
                'japadog',
                '.',
    ]

    bigrams = [
                ('You', 'want'),
                ('want', 'something'),
                ('something', 'memorable'),
                ('memorable', 'and'),
                ('and', 'weird'),
                ('weird', ','),
                (',', 'go'),
                ('go', 'check'),
                ('check', 'out'),
                ('out', 'japadog'),
    ]

    trigrams = [
                    ('You', 'want', 'something'),
                    ('want', 'something', 'memorable'),
                    ('something', 'memorable', 'and'),
                    ('memorable', 'and', 'weird'),
                    ('and', 'weird', ','),
                    ('weird', ',', 'go'),
                    (',', 'go', 'check'),
                    ('go', 'check', 'out'),
                    ('check', 'out', 'japadog'),
                    ('out', 'japadog', '.')
    ]

    quadgrams = [
                    ('You', 'want', 'something', 'memorable'),
                    ('want', 'something', 'memorable', 'and'),
                    ('something', 'memorable', 'and', 'weird'),
                    ('memorable', 'and', 'weird', ','),
                    ('and', 'weird', ',', 'go'),
                    ('weird', ',', 'go', 'check'),
                    (',', 'go', 'check', 'out'),
                    ('go', 'check', 'out', 'japadog'),
                    ('check', 'out', 'japadog', '.'),
    ]

    sentences = ['You want something memorable and weird,  go check out japadog.',]

    tweets = ['You want something memorable and weird,  go check out japadog.',]

    hashtags = [
                    'keepgoing',
                    'teamtank',
                    'apothicred',
                    'deleteuber',
    ]

    timeline = '{a string containing a big pile of JSON}'

    author = 'joey_testcase'

    last_tweet_id = '834085405318262784'


class TwitterUserFixture:
    """ Mock TwitterUser class for use in API testing """

    name = 'joey_testcase'
    description = r'Mustard lovin son of a gun'
    image = r'https://pbs.twimg.com/profile_images/758384037589348352/KB3RFwFm.jpg'


class TestEXCorpus(TestCase):
    """ Test sources.Corpus model for Excerpt type"""

    def setUp(self):
        attrs = {
                'title': 'Middle school girls dream journals',
                'body': 'Today I dreamt of a dancing coyote. Dylan wrote me a note in class',
                'variety': 'EX',
        }

        self.corpus = mixer.blend('sources.Corpus', **attrs)

    def test_ex_corpus_create(self):
        self.assertEqual(self.corpus.id, 1, 'Test corpus should have id=1')


class TestTWCorpus(TestCase):
    """ Test sources.Corpus model for Twitter type """
    """
    http://stackoverflow.com/questions/27667777/django-mocking-the-save-method-on-a-model
    """

    @patch('sources.models.Corpus')
    def setUp(self, mock_corpus):
        attrs = {
            'variety': 'TW',
            'twitter_username': 'jack',
        }

        self.corpus = mock_corpus(**attrs)

        # TODO: implement return_value of mock_corpus.save to return pickled Corpus object


    def test_tw_corpus_create(self):
        self.assertTrue(self.corpus.save.called, "Should have called mock save method of Corpus M")

    def test_tw_corpus_sentences(self):
        self.assertGreater(self.corpus.sentences.count(), 0, 'Test corpus should have sentences')





