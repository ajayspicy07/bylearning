



''' PROJECT URLS '''

from django.urls import path
from . import views

app_name = 'project'

urlpatterns = [
	path('<slug:slug>/createproject/', views.create_project, name="create-project"),
	path('projects/' , views.project.as_view(),             name=    'projects'),
	path('project/<slug:slug>/' , views.detail_project.as_view(), name='detail-project'),

	path('<slug:slug>/updateproject/', views.update_project, name="update-project"),
	path('<slug:slug>/deleteproject/', views.delete_project.as_view(), name="delete-project"),


	path('savedprojects/', views.saved_projects.as_view(), name="saved-projects"),


	path('<slug:slug>/projects/', views.profile_projects.as_view(), name="profile-projects"),

	path('projects/tags/<slug:slug>', views.tag_projects.as_view(), name="tag-projects"),


	
	path('createbanner/' , views.create_banner, name='create-banner'),
	path('banner/<slug:slug>/' , views.banner.as_view(), name='banner'),
	
	path('<slug:slug>/deletebanner/', views.delete_banner.as_view(), name="delete-banner"),
	


]