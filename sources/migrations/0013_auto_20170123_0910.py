# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-23 17:10
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sources', '0012_auto_20170122_1617'),
    ]

    operations = [
        migrations.RenameField(
            model_name='corpus',
            old_name='added_by',
            new_name='created_by',
        ),
    ]