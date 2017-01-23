from django import forms
from .models import Corpus, Word, Bigram, Trigram, Quadgram, Sentence


class CorpusForm(forms.ModelForm):
    """
    Form for handling user Corpus submission
    """
    class Meta:
        model = Corpus
        fields = ('twitter_username', 'variety', 'title', 'body', 'description', 'twitter_hashtag',)

    def __init__(self, *args, **kwargs):
        super(CorpusForm, self).__init__(*args, **kwargs)


        # With the two way form and post-processing, we don't want some of these fields required from the user side
        for key in self.fields:
            self.fields[key].required = False



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
