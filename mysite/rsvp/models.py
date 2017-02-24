from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class MyUser(models.Model):  
    user = models.OneToOneField(User)      
    phone = models.CharField(max_length=11)  
    def __unicode__(self):  
        return self.user.username   

class ConfeRoom(models.Model):  
    num = models.CharField(max_length=5)  
    name=models.CharField(max_length=50)  
    size=models.CharField(max_length=5)  
    acad=models.CharField(max_length=30)  
    class MEAT:                   
        ordering = ["num"]  
    def __unicode__(self):  
        return self.num  

class Detail(models.Model):  
    name = models.CharField(max_length=50)  
    img = models.ImageField(upload_to = "image")   
    time=models.CharField(max_length=20)  
    room = models.ForeignKey(ConfeRoom)     
    class MEAT:  
        ordering = ["name"]  
    def __unicode__(self):  
        return self.name  

class Order(models.Model):  
    user = models.CharField(max_length=30)  
    num=models.CharField(max_length=10)  
    name=models.CharField(max_length=50)  
    time=models.CharField(max_length=20)  
    size=models.CharField(max_length=5)  
    phone = models.CharField(max_length=11)  
    ntime = models.CharField(max_length=30)  
    def __unicode__(self):  
        return self.user 