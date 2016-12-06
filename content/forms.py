from django import forms
from .models import Mashup, Output


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
