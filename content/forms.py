from django import forms
from .models import Mashup, Output
from sources.models import Corpus


class MashupForm(forms.ModelForm):
    """
    Form for managing individual mashups
    """
    class Meta:
        model = Mashup
        fields = (
                 'title',
                 'description',
                 'algorithm',
                 'corpora'
                 )

    def __init__(self, *args, **kwargs):
        super(MashupForm, self).__init__(*args, **kwargs)
        self.fields["corpora"].widget = forms.widgets.CheckboxSelectMultiple(attrs={'id': 'selectable'})
        self.fields["corpora"].help_text = ""
        self.fields["corpora"].queryset = Corpus.objects.all()

        #widgets = {'corpora': forms.CheckboxSelectMultiple()}
