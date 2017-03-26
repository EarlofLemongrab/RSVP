from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


# MyUser is our class of user
# one MyUser instance can have three identities: one Owner instance,one Guest instance,one Vendor instances
class MyUser(models.Model):  
    user = models.OneToOneField(User)       
    name = models.CharField(max_length=50)
    email = models.EmailField(blank=True,null=True,max_length=50)

    def __unicode__(self):  
        return self.name

# Owner class describes all properties of owner 
class Owner(models.Model):
    user = models.OneToOneField(MyUser)

    def __unicode__(self):
        return self.user.name + "-Owner"

# Vendor class reflects vendor properties
class Vendor(models.Model):
    user = models.OneToOneField(MyUser)

    def __unicode__(self):
        return self.user.name + "-Vendor"

# Guest class models guest properties
class Guest(models.Model):
    user = models.OneToOneField(MyUser)

    def __unicode__(self):
        return self.user.name + "-Guest"

# An Event instance can have many owners, vendors as well as guests. An owner can have many events. 
# A guest can also have many events. A vendor can also have many events.
# So I use ManyToManyField to describe their relations.
class Event(models.Model):
    owners = models.ManyToManyField(Owner, blank = True)
    vendors = models.ManyToManyField(Vendor,blank = True)
    guests = models.ManyToManyField(Guest, blank = True)
    name = models.CharField(max_length=50)
    date = models.DateField(null = True, blank = True)
    location = models.CharField(max_length=200,default='')
    plusone = models.BooleanField(null= False, blank = False)

    def __unicode__(self):
        return self.name

#Model for multiple choice questions
class ChoiceQuestion(models.Model):
    event = models.ForeignKey(Event,on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200)
    vendors = models.ManyToManyField(Vendor,blank=True)
    finalized = models.BooleanField(blank=False,null=False)

    def __unicode__(self):
        return self.question_text

#Model for choices; A multiple choice can have many choices while one choice normally has one question.
class Choice(models.Model):
    question = models.ForeignKey(ChoiceQuestion, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    def __unicode__(self):
        return self.choice_text    

#Model for response: Record user and their choices
class ChoiceResponse(models.Model):
    user_choice = models.ForeignKey(Choice,on_delete=models.CASCADE)
    username = models.CharField(max_length=50,blank=True,null=True)

    def __unicode__(self):
        return self.username + "-ChoiceResponse"

#Model for TextQuestion
class TextQuestion(models.Model):
    event = models.ForeignKey(Event,on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200)
    vendors = models.ManyToManyField(Vendor,blank=True)
    finalized = models.BooleanField(blank=False,null=False)

    def __unicode__(self):
        return self.question_text

#Model for TextResponses
class TextResponse(models.Model):
    question = models.ForeignKey(TextQuestion,on_delete=models.CASCADE)
    response_text = models.CharField(max_length=200,default="Not answered yet")
    username = models.CharField(max_length=50,blank=True,null=True)

    def __unicode__(self):
        return self.response_text

#Model for Message
class Msg(models.Model):
    sender = models.ForeignKey(MyUser,related_name='sender',on_delete=models.CASCADE)
    receiver = models.ForeignKey(MyUser,related_name='receiver',on_delete=models.CASCADE)
    subtitle = models.CharField(max_length=200,default="")
    content = models.CharField(max_length=200,default="")

    def __unicode__(self):
        return self.subtitle 
        

