

''' COMMENT URLS '''

from django.urls import path
from . import views

app_name = 'comment'

urlpatterns = [


	path('<slug:slug>/<str:model_type>/createcomment/', views.create_comment, name='create-comment'),
	path('deletecomment/', views.delete_comment, name='delete-comment'),

	path('createreply/', views.create_reply, name='create-reply'),
	path('deletereply/', views.delete_reply, name='delete-reply'),




	]