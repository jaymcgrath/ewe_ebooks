# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-15 00:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bots', '0004_auto_20170114_1528'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bot',
            name='consumer_key',
        ),
        migrations.RemoveField(
            model_name='bot',
            name='consumer_secret',
        ),
        migrations.AddField(
            model_name='bot',
            name='request_token',
            field=models.CharField(blank=True, help_text='temporary key from oauth', max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='bot',
            name='request_token_secret',
            field=models.CharField(blank=True, help_text='temporary key from oauth', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='bot',
            name='access_token',
            field=models.CharField(blank=True, help_text='permanent access token for posting to twitter', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='bot',
            name='access_token_secret',
            field=models.CharField(blank=True, help_text='permanent access token secret for posting to twitter', max_length=255, null=True),
        ),
    ]