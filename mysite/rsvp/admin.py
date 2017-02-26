from django.contrib import admin

# Register your models here.  
from models import *  
  
admin.site.register(MyUser)  
admin.site.register(Event)
admin.site.register(Owner)
admin.site.register(Vendor)
admin.site.register(Guest)