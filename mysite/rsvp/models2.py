from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class MyUser(models.Model):  
    user = models.OneToOneField(User)      
    phone = models.CharField(max_length=11)  
    name = models.CharField(max_length=50)
    email = models.EmailField()

    def __unicode__(self):  
        return self.user.username   

class Owner(models.Model):
    user = models.OneToOneField(MyUser,on_delete=models.CASCADE)

class Vendor(models.Mode):
    user = models.OneToOneField(MyUser,on_delete=models.CASCADE)

class Guest(models.Model):
    user = models.OneToOneField(MyUser,on_delete=models.CASCADE)

class Event(models.Model):
	owners =  models.ForeignKey(MyUser,on_delete=models.CASCADE)
	vendors = models.ForeignKey(MyUser,on_delete=models.CASCADE)
	guests =  models.ForeignKey(MyUser,on_delete=models.CASCADE)

class Question(models.Model):
	event = models.ForeignKey(Event, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)


