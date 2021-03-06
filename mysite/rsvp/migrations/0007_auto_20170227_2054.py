# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-02-27 20:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rsvp', '0006_auto_20170226_2219'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChoiceQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.CharField(max_length=200)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rsvp.Event')),
            ],
        ),
        migrations.CreateModel(
            name='ChoiceResponse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TextQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.CharField(max_length=200)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rsvp.Event')),
            ],
        ),
        migrations.CreateModel(
            name='TextResponse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('response_text', models.CharField(max_length=200)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rsvp.TextQuestion')),
            ],
        ),
        migrations.RemoveField(
            model_name='question',
            name='event',
        ),
        migrations.RemoveField(
            model_name='choice',
            name='votes',
        ),
        migrations.AlterField(
            model_name='choice',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rsvp.ChoiceQuestion'),
        ),
        migrations.DeleteModel(
            name='Question',
        ),
        migrations.AddField(
            model_name='choiceresponse',
            name='user_choice',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rsvp.Choice'),
        ),
    ]
