# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-16 05:08
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bots', '0006_tweet'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Tweet',
            new_name='TwitterStatus',
        ),
    ]