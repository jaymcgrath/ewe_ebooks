from django.contrib import admin
from .models import Bot


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
            'mashup'
    )

admin.site.register(Bot, BotAdmin)
