from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User



class MyUser(models.Model):  
    user = models.OneToOneField(User)       
    name = models.CharField(max_length=50)
    email = models.EmailField(blank=True,null=True,max_length=50)

    def __unicode__(self):  
        return self.name   

class Owner(models.Model):
    user = models.OneToOneField(MyUser)

class Vendor(models.Model):
    user = models.OneToOneField(MyUser)


class Guest(models.Model):
    user = models.OneToOneField(MyUser)



class Event(models.Model):
    owners = models.ManyToManyField(Owner, blank = True)
    vendors = models.ManyToManyField(Vendor,blank = True)
    guests = models.ManyToManyField(Guest, blank = True)
    name = models.CharField(max_length=50)
    date = models.DateTimeField(null = True, blank = True)

    def __unicode__(self):
        return self.name

class Question(models.Model):
    event = models.ForeignKey(Event)
    question_text = models.CharField(max_length=50)

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
