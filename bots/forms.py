from django import forms
from .models import Bot, Tweet


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
                'mashup',
                 )

class TweetForm(forms.ModelForm):
    """
    Passthrough form for creating a tweet
    """

    class Meta:
        model = Tweet
        fields = (
                'bot',
                'output',
        )