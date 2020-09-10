
''' COMMENT VIEWS '''


from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse

from django.views.decorators.csrf import csrf_exempt

from .models import *
from user.models import Profile
from post.models import *
from project.models import Project, ProjectBanner

import re
# Create your views here.

''' some logic '''


@csrf_exempt
def create_comment(request,slug, model_type ):
    
    profile = Profile.objects.get(slug=request.user.username)
    
    question =request.GET.get('question',None)
    

    message=''

    if model_type == 'posts':
        post = Post.objects.get(slug=slug)
        comment = Comment.objects.create(content_object=post,user=profile,question=question)
        message = 'Created'
    elif model_type == 'projects':
        project = Project.objects.get(slug=slug)
        comment = Comment.objects.create(content_object=project,user=profile,question=question)
        message = 'Created'
   
    else :
        banner = ProjectBanner.objects.get(slug=slug)
        comment = Comment.objects.create(content_object=banner,user=profile,question=question)
        message = 'Created'
   

    if message == 'Created':
         profile_values =  {
            'name': str(comment.user), 
            'image': comment.user.image.url,
            'slug' : comment.user.slug,
            'comment': comment.question,
            'id': comment.id
        }
    else:
        profile_values =[]

    return JsonResponse(profile_values,safe=False)


@csrf_exempt
def delete_comment(request):
    id =request.GET.get('id',None)
    

    comment = Comment.objects.get(id = id)
    if comment:
        comment.delete()
        message = 'Deleted'
    
    return JsonResponse(message,safe=False)

@csrf_exempt
def create_reply(request):
    profile = Profile.objects.get(slug=request.user.username)
    id =request.GET.get('id',None)
    reply = request.GET.get('reply',None)

    comment = Comment.objects.get(id = id)
    
    message = ''
    if comment :
        reply = Reply.objects.create(user=profile, for_comment = comment, answer = reply)
        message = 'Created'
    if message == 'Created':
        profile_values =  {
            'name': str(reply.user), 
            'image': reply.user.image.url,
            'slug' : reply.user.slug,
            'comment': reply.answer,
            'id': reply.id
        }
    else:
        profile_values = []
    
    return JsonResponse(profile_values,safe=False)


@csrf_exempt
def delete_reply(request):
    id =request.GET.get('id',None)
    
    reply = Reply.objects.get(id = id)
    print(reply)
    if reply:
        reply.delete()
        message = 'Deleted'
    
    return JsonResponse(message,safe=False)
