from django import forms
from .models import Corpus, Word, Bigram, Trigram, Quadgram, Sentence, Hashtag


class CorpusForm(forms.ModelForm):
    """
    Form for testing a Corpus before database insertion
    """
    class Meta:
        model = Corpus
        fields = ('twitter_username',)


class WordForm(forms.ModelForm):
    class Meta:
        model = Word
        fields = ('word',)


class BigramForm(forms.ModelForm):
    class Meta:
        model = Bigram
        fields = ('word1', 'word2')


class TrigramForm(forms.ModelForm):
    class Meta:
        model = Trigram
        fields = ('word1', 'word2', 'word3')


class QuadgramForm(forms.ModelForm):
    class Meta:
        model = Quadgram
        fields = ('word1', 'word2', 'word3', 'word4')


class SentenceForm(forms.ModelForm):
    class Meta:
        model = Sentence
        fields = ('sentence',)
