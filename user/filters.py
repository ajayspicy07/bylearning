 
''' POST FILETERS '''

import django_filters
from .models import Post
from user.models import User,Profile
from django.db.models import Q

import operator
from functools import reduce


class PostFilter(django_filters.FilterSet):

	

	title = django_filters.CharFilter(label='Search', method= 'filter_by_search')

	

	def __init__(self,*args, **kwargs):
		self.user = kwargs.pop('user')
		super(PostFilter,self).__init__(*args,**kwargs)

	def filter_by_search(self,queryset,name,value):
		search_list=value.split()
		query = reduce(operator.and_ , (Q(title__icontains = item) for item in search_list))
		main_queryset =  queryset.filter(query)
		
		if main_queryset.count()<=10:
			for search_terms in search_list:
				second_queryset=queryset.filter(title__icontains=search_terms)
				main_queryset=main_queryset|second_queryset
		return main_queryset 




	class Meta:
 		model = Post
 		fields = ('title',)

 

