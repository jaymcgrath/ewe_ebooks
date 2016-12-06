import pytest
from mixer.backend.django import mixer
from datetime import datetime

# Remove safety switch that prevents hitting the db (even the test db)
pytestmark = pytest.mark.django_db

corpus = mixer.blend('sources.Corpus', added=datetime.now(), twitter_username='jack')

class TestCorpus:
    def test_corpus_create(self):
        assert corpus.id == 1, 'Should save an instance'

