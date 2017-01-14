from django import forms

from .models import Mashup


class MashupForm(forms.ModelForm):
    """
    Form for creating a mashup
    """
    class Meta:
        model = Mashup
        fields = (
                 'title',
                 'description',
                 'algorithm',
                 'corpora'
                 )