from django.contrib import admin
from .models import Corpus, Word, Bigram, Trigram, Quadgram, Sentence, Hashtag
# Register your models here.

admin.site.register(Corpus)
admin.site.register(Word)
admin.site.register(Bigram)
admin.site.register(Trigram)
admin.site.register(Quadgram)
admin.site.register(Sentence)
admin.site.register(Hashtag)
