from django import forms


class CorpusForm(forms.ModelForm):
    """
    Form for testing a Corpus before database insertion
    """
    class Meta:
        model = 'sources.Corpus'
        fields = (
                 'title',
                 'desc',
                 'is_public',
                 'type',
                 'twitter_username',
                 'author',
                 'mash_count'
                 )


class WordForm(forms.ModelForm):
    class Meta:
        model = 'sources.Word'
        fields = ('word',)


class BigramForm(forms.ModelForm):
    class Meta:
        model = 'sources.Bigram'
        fields = ('word1', 'word2')


class TrigramForm(forms.ModelForm):
    class Meta:
        model = 'sources.Trigram'
        fields = ('word1', 'word2', 'word3')


class QuadgramForm(forms.ModelForm):
    class Meta:
        model = 'sources.Quadgram'
        fields = ('word1', 'word2', 'word3', 'word4')


class SentenceForm(forms.ModelForm):
    class Meta:
        model = 'sources.Sentence'
        fields = ('sentence',)
