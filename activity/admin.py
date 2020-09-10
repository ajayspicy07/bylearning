

''' ACTIVITY ADMIN '''

from django.contrib import admin
from .models import * 

# Register your models here.

class LikeAdmin(admin.ModelAdmin):
	list_display=('content_object', 'content_type' , 'user')
	search_fields=('content_object',)
	



class SavedAdmin(admin.ModelAdmin):
	list_display=('user', 'content_object' ,'content_type','date_created')
	search_fields=('content_object',)
	list_filter=('user','date_created')
	ordering =('date_created',)

  
  
admin.site.register(Like,LikeAdmin)

admin.site.register(Saved,SavedAdmin)

