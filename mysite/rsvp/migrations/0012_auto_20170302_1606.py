# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-03-02 16:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rsvp', '0011_event_plusone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
