# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-16 04:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0020_auto_20170114_1526'),
        ('bots', '0005_auto_20170114_1642'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tweet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_id', models.BigIntegerField(help_text='twitter status ID of this tweet')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='local timestamp')),
                ('created_twitter', models.DateTimeField(help_text='twitter creation timestamp', null=True)),
                ('text', models.CharField(help_text='the actual body of the tweet as posted on twitter', max_length=157)),
                ('retweet_count', models.IntegerField(default=0, help_text='the number of retweets this tweet has received')),
                ('screen_name', models.CharField(help_text='screen_name of the account that posted this', max_length=16)),
                ('bot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tweets', to='bots.Bot')),
                ('mashup', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tweets', to='content.Mashup')),
                ('output', models.ForeignKey(help_text='the output object posted to twitter', on_delete=django.db.models.deletion.CASCADE, related_name='tweets', to='content.Output')),
            ],
        ),
    ]
