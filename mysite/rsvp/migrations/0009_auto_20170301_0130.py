# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-03-01 01:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rsvp', '0008_auto_20170228_1948'),
    ]

    operations = [
        migrations.AlterField(
            model_name='textresponse',
            name='response_text',
            field=models.CharField(default='Not answered yet', max_length=200),
        ),
    ]
