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
    url(r'^guestdetails/$',views.guestdetails),
    url(r'^vendordetails/$',views.vendordetails),
    url(r'^textfinalized/$',views.textfinalized),
    url(r'^choicefinalized/$',views.choicefinalized),
    url(r'^addtextvendor/$',views.addtextvendor),
    url(r'^addchoicevendor/$',views.addchoicevendor),
    url(r'^edittextresponse/$',views.edittextresponse),
    url(r'^editchoiceresponse/$',views.editchoiceresponse),
    url(r'^textquestiondetails/$',views.textquestiondetails),
    url(r'^choicequestiondetails/$',views.choicequestiondetails),
    url(r'^addchoice/$',views.addchoice),
    url(r'^textquestionedit/$',views.textquestionedit),
    url(r'^choicequestionedit/$',views.choicequestionedit),
]
