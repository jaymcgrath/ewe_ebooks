from django import forms
from .models import Bot


class BotForm(forms.ModelForm):
    """
    Form for first step in creating a Bot
    """

    class Meta:
        model = Bot
        fields = (
                'name',
                'description',
                'post_frequency',
                 )