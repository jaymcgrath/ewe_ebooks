# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-05 20:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0002_mashup_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mashup',
            name='algorithm',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='algo', to='content.MashupAlgorithm'),
        ),
    ]
