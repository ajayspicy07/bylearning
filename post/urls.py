

''' POST URLS '''

from django.urls import path
from . import views

app_name = 'post'

urlpatterns = [
	path('<slug:slug>/createpost/', views.create_post, name="create-post"),
	path('posts/' , views.posts.as_view(),             name=    'posts'),
	path('post/<slug:slug>/' , views.detail_post.as_view(), name='detail-post'),

	path('<slug:slug>/updatepost/', views.update_post, name="update-post"),
	path('<slug:slug>/deletepost/', views.delete_post.as_view(), name="delete-post"),


	

	path('<slug:slug>/posts/', views.profile_posts.as_view(), name="profile-posts"),

	path('posts/tags/<slug:slug>', views.tag_posts.as_view(), name="tag-posts"),

	path('savedposts/', views.saved_posts.as_view(), name="saved-posts"),


	
	path('<slug:slug>/createfolder/' , views.create_folder, name='create-folder'),
	path('folder/<slug:slug>/' , views.folder.as_view(), name='folder'),
	path('<slug:slug>/addpost-folder/', views.create_post_for_folder, name="create-post-folder"),
	
	path('<slug:slug>/deletefolder/', views.delete_folder.as_view(), name="delete-folder"),


	path('<slug:slug>/folders/', views.profile_folders.as_view(), name="profile-folders"),



	path('tag-auto-complete/', views.tagautocomplete, name = "tag-auto-complete"),
	
   

]