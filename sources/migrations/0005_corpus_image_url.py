# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-06 22:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sources', '0004_auto_20161205_1640'),
    ]

    operations = [
        migrations.AddField(
            model_name='corpus',
            name='image_url',
            field=models.CharField(max_length=256, null=True),
        ),
    ]
