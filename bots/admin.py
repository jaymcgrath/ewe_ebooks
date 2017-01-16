from django.contrib import admin
from .models import Bot, TwitterStatus


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

class TwitterStatusAdmin(admin.ModelAdmin):
    fields = (
            'item_id',
            'created_twitter',
            'bot',
            'mashup',
            'output',
            'text',
            'retweet_count',
            'screen_name',
    )

admin.site.register(Bot, BotAdmin)
admin.site.register(TwitterStatus, TwitterStatusAdmin)
