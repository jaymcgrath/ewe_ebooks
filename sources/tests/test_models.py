import pytest
from mixer.backend.django import mixer
from sources.models import Corpus
from datetime import datetime

# Remove safety switch that prevents hitting the db (even the test db)
pytestmark = pytest.mark.django_db

class TestPost:
    def test_corpus_create(self):
        corpus = mixer.blend('sources.Corpus',added=datetime.now())
        assert corpus.id == 1, 'Should save an instance'
