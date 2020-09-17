

''' USER DECORATORS '''

from django.shortcuts import render, redirect
from django.http import HttpResponse,JsonResponse
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from .models import *
from post.models import PostDirectory , Post
from project.models import Project

def authenticated_user(view_function):

	def wrapper_function(request,*args, **kwargs):
		if request.user.is_authenticated:
			return redirect('user:home')
		else:
			return view_function(request, *args, **kwargs)


	return wrapper_function

# for post folder  project creation whick passes the profile slug
def permission(view_function):

	def wrapper_function(request,slug,*args, **kwargs):

		profile = get_object_or_404(Profile,slug=slug)
		login_user = request.user.user
		
		if profile.content_object.is_page():
			members  = profile.content_object.members.all()
			if login_user in members or login_user == profile.content_object.admin:
				return view_function(request,slug, *args, **kwargs)
			
			else:
				raise PermissionDenied
		else:
			if login_user.username == profile.content_object.username:
				return view_function(request,slug, *args, **kwargs)
			else:
				raise PermissionDenied



	return wrapper_function


#for folder post creation
def folder_post_permission(view_function):

	def wrapper_function(request,slug,*args, **kwargs):

		folder  = get_object_or_404(PostDirectory,slug=slug)
		login_user = request.user.user
		profile = folder.owner

		if profile.content_object.is_page():
			members  = profile.content_object.members.all()
			if login_user in members or login_user == profile.content_object.admin:
				return view_function(request,slug, *args, **kwargs)
			
			else:
				raise PermissionDenied
		else:
			if login_user.username == profile.content_object.username:
				return view_function(request,slug, *args, **kwargs)
			else:
				raise PermissionDenied



	return wrapper_function

#updation permission post
def update_post_permission(view_function):

	def wrapper_function(request,slug,*args, **kwargs):

		post  = get_object_or_404(Post,slug=slug)
		login_user = request.user.user
		profile = post.author

		if profile.content_object.is_page():
			members  = profile.content_object.members.all()
			if login_user in members or login_user == profile.content_object.admin:
				return view_function(request,slug, *args, **kwargs)
			
			else:
				raise PermissionDenied
		else:
			if login_user.username == profile.content_object.username:
				return view_function(request,slug, *args, **kwargs)
			else:
				raise PermissionDenied



	return wrapper_function

#updation permission Project
def update_project_permission(view_function):

	def wrapper_function(request,slug,*args, **kwargs):

		project  = get_object_or_404(Project,slug=slug)
		login_user = request.user.user
		profile = project.author

		if profile.content_object.is_page():
			members  = profile.content_object.members.all()
			if login_user in members or login_user == profile.content_object.admin:
				return view_function(request,slug, *args, **kwargs)
			
			else:
				raise PermissionDenied
		else:
			if login_user.username == profile.content_object.username:
				return view_function(request,slug, *args, **kwargs)
			else:
				raise PermissionDenied



	return wrapper_function

#updation permission Profile
def update_profile_permission(view_function):

	def wrapper_function(request,slug,*args, **kwargs):

		profile  = get_object_or_404(Profile,slug=slug)
		login_user = request.user.user
	

		if profile.content_object.is_page():
			members  = profile.content_object.members.all()
			if login_user in members or login_user == profile.content_object.admin:
				return view_function(request,slug, *args, **kwargs)
			
			else:
				raise PermissionDenied
		else:
			if login_user.username == profile.content_object.username:
				return view_function(request,slug, *args, **kwargs)
			else:
				raise PermissionDenied



	return wrapper_function