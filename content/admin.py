from django.contrib import admin
from .models import MashupAlgorithm, Mashup, Output, Bot


class BotAdmin(admin.ModelAdmin):
    fields = (
            'name',
            'description',
            'post_frequency',
            'consumer_key',
            'consumer_secret',
            'access_token',
            'access_token_secret',
            'mashup',
    )

# Register your models here.

admin.site.register(MashupAlgorithm)
admin.site.register(Mashup)
admin.site.register(Output)
admin.site.register(Bot, BotAdmin)
