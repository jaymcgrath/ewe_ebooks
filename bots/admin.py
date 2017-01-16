from django.contrib import admin
from .models import Bot, Tweet


class BotAdmin(admin.ModelAdmin):
    fields = (
            'name',
            'description',
            'post_frequency',
            'request_token',
            'request_token_secret',
            'access_token',
            'access_token_secret',
            'user',
            'mashup',
    )

class TweetAdmin(admin.ModelAdmin):
    fields = (
            'tweet_id',
            'created_twitter',
            'bot',
            'output',
            'text',
            'retweet_count',
            'screen_name',
    )

admin.site.register(Bot, BotAdmin)
admin.site.register(Tweet, TweetAdmin)
