





''' PROJECT ADMIN '''
from django.contrib import admin
from post.admin import PostProjectAdmin
from .models import *
# Register your models here.



class  ProjectAdmin(PostProjectAdmin):
	pass


class ProjectBannerAdmin(admin.ModelAdmin):
  
	list_display=('heading', 'slug' , 'owner', 'date_created')

	list_filter=('owner',)
	search_fields=('heading',)
	ordering =('date_created',)





admin.site.register(Project,ProjectAdmin)

admin.site.register(ProjectBanner,ProjectBannerAdmin)