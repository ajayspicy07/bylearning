

''' USER ADMIN '''

from django.contrib import admin
from django.contrib.auth.models import User 
from .models import *
#from .forms import *

# Register your models here.

''' college admin '''
class CollegeAdmin(admin.ModelAdmin):
	list_display = ('name','district' ,'state')
	list_filter = ('district', 'state')


''' user admin '''  
class UserAdmin(admin.ModelAdmin):
	list_display=('full_name','username', 'get_college_name','email' , 'user_mode', 'dob')
	list_filter =('user_mode',)

	def get_college_name(self, obj):
		if obj.college:
			return obj.college.name
		else:
			return 'College deleted'
	get_college_name.short_description = 'College'
  

class PageAdmin(admin.ModelAdmin):
	list_display = ('name', 'get_members','college', 'date_created')
	list_filter= ('college', )

	def get_members(self, obj):
		return "\n,".join([p.full_name() for p in obj.members.all()])
	get_members.short_description = 'members'


class ProfileAdmin(admin.ModelAdmin):
	list_display =('get_name', 'get_college','get_type' , 'type_created')

	def get_name(self,obj):
		return obj

	def get_type(self,obj):
		return obj.content_type.name

	def type_created(self,obj):
		return obj.content_object.date_created

	def get_college(self,obj):
		return obj.content_object.college
  
	get_name.short_description = 'name'
	get_type.short_description = 'type'
	get_college.short_description = 'college'


class FollowerAdmin(admin.ModelAdmin):
	list_display =('from_profile', 'to_profile','date_created')
	list_filter = ('from_profile', 'to_profile')
  

admin.site.register(College,CollegeAdmin)

admin.site.register(User,UserAdmin)

admin.site.register(Page, PageAdmin)

admin.site.register(Profile, ProfileAdmin)

admin.site.register(Follower,FollowerAdmin)