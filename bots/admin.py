from django.contrib import admin
from .models import Bot


class BotAdmin(admin.ModelAdmin):
    fields = (
            'name',
            'description',
            'post_frequency',
            'consumer_key',
            'consumer_secret',
            'access_token',
            'access_token_secret',
            'user',
            'mashup'
    )

admin.site.register(Bot, BotAdmin)
