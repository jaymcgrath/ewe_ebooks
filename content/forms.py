from django import forms
from .models import Mashup

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

