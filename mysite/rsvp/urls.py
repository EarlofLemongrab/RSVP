from django.conf.urls import include, url                                     
from django.contrib import admin  
admin.autodiscover()  
from . import views

urlpatterns = [
    url(r'^$',views.index),  
    url(r'^regist/$',views.regist),  
    url(r'^login/$',views.login),  
    url(r'^logout/$',views.logout),   
    url(r'^events/$',views.events),  
    url(r'^ownerdetails/$',views.ownerdetails),  
    url(r'^create/$',views.create),
    url(r'^edit/$',views.edit),
    url(r'^add/$',views.add),
    url(r'^addq/$',views.addq),
    url(r'^guestdetails/$',views.guestdetails)
    #url(r'^addq/$',views.addquestion),
    #url(r'^ajax/validate_username/$', views.validate_username, name='validate_username'),
]