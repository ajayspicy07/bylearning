

''' ACTIVITY VIEWS '''


from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse

from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

from post.models import Post 
from project.models import Project
from user.models import Profile
from .models import *


# Create your views here.

@csrf_exempt
def like(request, slug, object_type):
	profile = Profile.objects.get(slug=request.user.username)
	if request.method == 'POST':
		if object_type == 'True':
			project = Project.objects.get(slug=slug)
			if Like.objects.filter(Q(projectlikes__slug=project.slug)& Q(user=profile.id)).exists():
				Like.objects.filter(projectlikes__slug=project.slug, user=profile.id).delete()
				message='Deleted'
				
				project.likes = project.likes -1
				project.save()
			

			else:
				Like.objects.create(content_object=project, user=profile)
				message='Created'
				
				project.likes = project.likes +1
				project.save()
				
			
			
		else:
			post = Post.objects.get(slug=slug)
			if Like.objects.filter(Q(postlikes__slug=post.slug)& Q(user=profile.id)).exists():
				Like.objects.filter(postlikes__slug=post.slug, user=profile.id).delete()
				message='Deleted'
				
				post.likes = post.likes -1
				post.save()
			

			else:
				Like.objects.create(content_object=post, user=profile)
				message='Created'
				
				post.likes = post.likes +1
				post.save()
				
			
				
	
	
	return JsonResponse(message, safe = False)
        




@csrf_exempt
def save(request, slug, object_type):
	profile = Profile.objects.get(slug=request.user.username)

	if request.method == 'POST':
	
		if object_type == 'True':
			
			project = Project.objects.get(slug=slug)
			if Saved.objects.filter(Q(projectsaved__slug=project.slug)& Q(user=profile.id)).exists():
				Saved.objects.filter(projectsaved__slug=project.slug, user=profile.id).delete()
				message='Deleted'
			else:
				Saved.objects.create(content_object=project, user=profile)
				message='Created'
			
			
		else:
		
			post = Post.objects.get(slug=slug)
			print(post)
			if Saved.objects.filter(Q(postsaved__slug=post.slug)& Q(user=profile.id)).exists():
				Saved.objects.filter(postsaved__slug=post.slug, user=profile.id).delete()
				message = 'Deleted'
			else:
				Saved.objects.create(content_object=post, user=profile)
				message='Created'

				
	
	
	return JsonResponse(message, safe = False)
        
