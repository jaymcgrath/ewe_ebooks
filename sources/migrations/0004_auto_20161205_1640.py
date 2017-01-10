# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-06 00:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sources', '0003_auto_20161205_1226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sentence',
            name='corpus',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sentences', to='sources.Corpus'),
        ),
    ]