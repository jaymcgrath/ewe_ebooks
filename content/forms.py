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
        # widget = {'title': forms.Select(choices=((1,)), attrs={'class': 'myclass', 'placeholder': 'zipcode'})}

    def __init__(self, *args, **kwargs):
        super(MashupForm, self).__init__(*args, **kwargs)

        # Set some additional field attributes

        title_attrs = {
                'class': 'form-control',
                'placeholder': 'Mashup Title',
                'aria-label': 'Input the mashup title',
                }
        self.fields['title'].widget.attrs.update(title_attrs)

        desc_attrs = {
                'class':'form-control',
                'placeholder': 'A brief description of this mashup',
                'aria-label': 'Input for mashup description'
                }
        self.fields['description'].widget.attrs.update(desc_attrs)

        algo_attrs = {
                'class':'form-control',
                'aria-label': 'The method used to combine text'
        }
        self.fields['algorithm'].widget.attrs.update(algo_attrs)



