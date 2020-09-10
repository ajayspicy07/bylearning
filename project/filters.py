 
''' PROJECT FILETERS '''

import django_filters
from .models import Project
from user.models import User,Profile
from django.db.models import Q

import operator
from functools import reduce


class ProjectFilter(django_filters.FilterSet):

	SORT_CHOICES=(
	('latest','Latest'),
	('views', 'Views'),
	('appreciations','Appreciations')
	)

	FILTER_CHOICES=(
	('all','All Projects'),
	('college', 'My College'),
	('following','Following')
	)

	title = django_filters.CharFilter(label='Search', method= 'filter_by_search')

	sorting = django_filters.ChoiceFilter(label='Sort by',
		choices= SORT_CHOICES, method ='filter_by_sort', empty_label=None)

	filtering = django_filters.ChoiceFilter(label='Filter by',
		choices= FILTER_CHOICES, method ='filter_by_filter', empty_label=None)


	def __init__(self,*args, **kwargs):
		self.user = kwargs.pop('user')
		super(ProjectFilter,self).__init__(*args,**kwargs)

	def filter_by_search(self,queryset,name,value):
		search_list=value.split()
		query = reduce(operator.and_ , (Q(title__icontains = item) for item in search_list))
		main_queryset =  queryset.filter(query)
		
		if main_queryset.count()<=10:
			for search_terms in search_list:
				second_queryset=queryset.filter(title__icontains=search_terms)
				main_queryset=main_queryset|second_queryset
		return main_queryset 



	def filter_by_sort(self,queryset,name,value):
		if value=='latest':
			sort_by='-date_created'

		elif value=='views':

			sort_by = '-views'
		else:
			sort_by = '-likes'
		return queryset.order_by(sort_by)

	

	def filter_by_filter(self,queryset,name,value):
		if value=='all':
			return queryset
		elif value=='college':
			college = self.user.user.college
			return queryset.filter(Q(author__users__college__name=college)|
				Q(author__pages__college__name=college))
    
		else:
			sort_by = 'following'
			user_id = self.user.user.user.id 
			profile_instance = Profile.objects.get(users__id = user_id)
			follower_instances = profile_instance.followers.all()
			following_list=[]
			for i in follower_instances:
				following_list.append(i.to_profile)
			return queryset.filter(author__in = following_list)

	class Meta:
 		model = Project
 		fields = ('title',)

 

