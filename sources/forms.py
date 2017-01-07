from django import forms
from .models import Corpus, Word, Bigram, Trigram, Quadgram, Sentence


class CorpusForm(forms.ModelForm):
    """
    Form for testing a Corpus before database insertion
    """
    class Meta:
        model = Corpus
        fields = ('twitter_username', 'variety', 'title', 'body', 'description',)

    def __init__(self, *args, **kwargs):
        super(CorpusForm, self).__init__(*args, **kwargs)

        # Set some additional field attributes

        variety_attrs = {
                'class': 'form-control',
                'placeholder': 'Source Type',
                'aria-label': 'Input the source type',
                'id': 'variety'
                }
        self.fields['variety'].widget.attrs.update(variety_attrs)

        desc_attrs = {
                'class':'form-control',
                'placeholder': 'A brief description of this source',
                'aria-label': 'Input for source description'
                }
        self.fields['description'].widget.attrs.update(desc_attrs)

        title_attrs = {
                'class':'form-control',
                'placeholder': 'Choose a title for this source',
                'aria-label': 'Input for source title'
        }
        self.fields['title'].widget.attrs.update(title_attrs)

        body_attrs = {
            'class': 'form-control',
            'placeholder': 'Paste the body of the excerpt here',
            'aria-label': 'Input for source body'
        }
        self.fields['body'].widget.attrs.update(body_attrs)

        twitter_username_attrs = {
            'type':'text',
            'placeholder':"username",
            'aria-describedby':"username1"
        }
        self.fields['twitter_username'].widget.attrs.update(twitter_username_attrs)


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
