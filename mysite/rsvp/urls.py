from django.conf.urls import patterns, include, url  
from rsvp import views                                      
from django.contrib import admin  
admin.autodiscover()  
from . import views

urlpatterns = [
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),  
    url(r'^admin/', include(admin.site.urls)),  
    url(r'^$',views.index),  
    url(r'^regist/$',views.regist),  
    url(r'^login/$',views.login),  
    url(r'^logout/$',views.logout),  
    url(r'^cancel/$',views.cancel),  
    url(r'^myorder/$',views.myorder),  
    url(r'^viewroom/$',views.viewroom),  
    url(r'^detail/$',views.detail),  
    url(r'^order/$',views.order),  
]