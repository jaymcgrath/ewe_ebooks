# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-30 18:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0009_auto_20161222_1134'),
    ]

    operations = [
        migrations.AddField(
            model_name='bot',
            name='description',
            field=models.TextField(help_text='A brief description of how this bot looks on Twitter', null=True),
        ),
    ]
