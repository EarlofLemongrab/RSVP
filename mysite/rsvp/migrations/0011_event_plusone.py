# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-03-01 19:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rsvp', '0010_auto_20170301_1902'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='plusone',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]