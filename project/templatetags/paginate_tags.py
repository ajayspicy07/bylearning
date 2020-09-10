

''' TEMPLATE TAGS IN POSTS  '''
from django.db.models import Q
from django import template

from user.models import Profile
from project.models import *
from activity.models import *

register = template.Library()


@register.simple_tag
def my_paginate_url(value,field_name,urlencode=None):
	url = '?{}={}'.format(field_name,value)
	
	if urlencode and urlencode[:4]!='page':
		url = '{}={}'.format(field_name,value)
	
		querystring = urlencode.split('&')
		filtered_querystring = filter(lambda p:p.split('=')[0]!=field_name,querystring)
	
		encoded_querystring = '&'.join(filtered_querystring)
		url = '?{}&{}'.format(encoded_querystring,url)

	return url


@register.simple_tag
def is_saved_project(slug,user):
	
	profile = Profile.objects.get(users__username=user)
	
	
	if Saved.objects.filter(Q(projectsaved__slug=slug)& Q(user= profile.id)).exists():
		return True

	else :
		False

@register.simple_tag
def is_saved_post(slug,user):

	
	profile = Profile.objects.get(users__username=user)
	
	
	if Saved.objects.filter(Q(postsaved__slug=slug)& Q(user= profile.id)).exists():
		return True

	else :
		False
	

	

@register.simple_tag
def is_liked_project(slug,user):
	
	profile = Profile.objects.get(users__username=user)
	
	
	if Like.objects.filter(Q(projectlikes__slug=slug)& Q(user= profile.id)).exists():
		return True

	else :
		False
	


@register.simple_tag
def is_liked_post(slug,user):
	
	profile = Profile.objects.get(users__username=user)
	
	
	if Like.objects.filter(Q(postlikes__slug=slug)& Q(user= profile.id)).exists():
		return True

	else :
		False
	







