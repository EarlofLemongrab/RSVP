# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-02-26 22:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rsvp', '0005_auto_20170226_2148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
