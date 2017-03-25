from django.contrib import admin

# Register your models here.  
from models import *  
  
admin.site.register(MyUser)  
admin.site.register(Event)
admin.site.register(Owner)
admin.site.register(Vendor)
admin.site.register(Guest)
admin.site.register(TextQuestion)
admin.site.register(ChoiceQuestion)
admin.site.register(TextResponse)
admin.site.register(ChoiceResponse)
admin.site.register(Choice)
admin.site.register(Msg)