# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-23 17:10
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bots', '0010_tweet_mashup'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bot',
            old_name='user',
            new_name='created_by',
        ),
    ]
