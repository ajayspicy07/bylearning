

''' Project VIEWS '''

from django.shortcuts import render, redirect
from django.http import HttpResponse,JsonResponse
from django.urls import reverse
from django.db.models import F


from django.contrib.auth.decorators import login_required, user_passes_test

from django.utils import timezone
from datetime import timedelta
from django.views.generic import CreateView,ListView,DetailView,UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger,InvalidPage
#from django_filters.views import FilterView
from slugify import UniqueSlugify,Slugify


from .models import *
from .forms import *
from .filters import *
from user.models import *
from comment.models import *
from activity.models import *
from user.decorators import *


''' SOME LOGIC '''
custom_slugify = Slugify()

@login_required
@permission
def create_project(request, slug):
	profile = Profile.objects.get(slug=slug)
	if request.method == 'POST':
		form =ProjectCreationForm(request.POST)
		
		if form.is_valid():
			form.instance.author = profile
			form.save()
			form.instance.slug  =custom_slugify(form.instance.title, 
				allow_unicode=True)+'-'+str(profile.id)+str(form.instance.id)
			form.save()

			data = form.cleaned_data['add_tags']
			for i in data.split('--')[:-1]:
				try:
					tag = Tag.objects.get(tag_name__iexact=i.strip())
				except:
					if i!=' ':
						tag = Tag.objects.create(tag_name=i.strip(),user_create=True)
						tag.save()
				form.instance.tags.add(tag)
			return redirect('project:detail-project', slug = form.instance.slug)
		
	else:
		form =ProjectCreationForm(request.POST)
	
	context ={'form':form, 'profile':profile}
	return render(request,'project/createproject.html',context)




class project(LoginRequiredMixin, ListView):
	model = Project
	template_name = 'project/projects.html'
	paginate_by = 10
	ordering =[ '-date_created']

	def get_queryset(self):
		projects = Project.objects.all().prefetch_related('tags','author')
		return projects
	

	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)
		college = self.request.user.user.college

		context['filter']= ProjectFilter(self.request.GET, 
			queryset=self.get_queryset().filter(Q(
				author__users__college__name = college)|Q(
				visibility='PUBLIC')|Q(author__pages__college__name=college)),
			user=self.request.user )

		paginated_filterd_projects = Paginator(context['filter'].qs,self.paginate_by)
		page_number = self.request.GET.get('page')
		projects_per_page = paginated_filterd_projects.get_page(page_number)
		context['projects_per_page'] = projects_per_page
		return context
 


	
class detail_project(LoginRequiredMixin, DetailView):
	model = Project
	template_name= 'project/projectdetail.html'
	

	def get_ip(self):
		address = self.request.META.get('HTTP_X_FORWARDED_FOR')
		if address:
			ip = address.split(',')[-1].strip()
		else:
			ip= self.request.META.get('REMOTE_ADDR')
		return ip

	def get_context_data(self,**kwargs):

		context = super().get_context_data(**kwargs)
		college = self.request.user.user.college
		slug = self.kwargs['slug']
		
		#project=Project.objects.get(slug=slug)
		project = get_object_or_404(Project.objects.prefetch_related(
				'author','tags'), slug=slug)
		
		key=project.slug
		session = self.request.session.get(key)
		if project.visibility == 'PUBLIC' or project.author.content_object.college == college:
			if self.request.user.is_authenticated and self.get_ip() and not session:
				#project.views+=1
				project.views = F('views')+1
				project.save()
				self.request.session[key]=True

		#comments = Comment.objects.filter(projects__slug= project.slug)
		if project.comments == "ENABLE":
			comments = Comment.objects.filter(
				projects__slug= project.slug).prefetch_related('user','replies')
		else: 
			comments =[]

		context={
			'project':project,
			'comments': comments,
		}

		return context
 


		

	'''
	def test_func(self):
		project = self.get_object()
		college = self.request.user.user.college
		if project.visibility == 'PUBLIC' or project.author.content_object.college == college:
			return True
		else:
			return False

	'''
class delete_project(LoginRequiredMixin, UserPassesTestMixin ,DeleteView):
	model = Project
	
	def get_success_url(self):
		slug = self.kwargs['slug']
		author = Project.objects.get(slug=slug).author.slug
		return reverse('project:profile-projects', kwargs= {'slug':author})

	def test_func(self):
		project = self.get_object()
		user = self.request.user.user
		profile = get_object_or_404(Profile, slug = user.username)

		if project.author.content_object.is_page():
			if user in project.author.content_object.members.all() or user == project.author.content_object.admin:
				return True
		else:
			if profile == project.author:
				return True
		return False




def create_banner(request):
	profile = Profile.objects.get(slug=request.user.username)
	if request.method == 'POST':
		form =BannerCreationForm(request.POST)
		
		if form.is_valid():
			form.instance.owner = profile

			form.save()
			print(profile.id)
			print(form.instance.id)
			form.instance.slug  = custom_slugify(form.instance.heading, 
				allow_unicode=True)+'-'+str(profile.id)+str(form.instance.id)
			form.save()
			print(form.instance.slug)
			return redirect('project:banner', slug = form.instance.slug )
		
	else:
		form =BannerCreationForm(request.POST)
	
	context ={'form':form, 'profile':profile}
	return render(request,'project/createbanner.html',context)

class banner(LoginRequiredMixin,DetailView):
	model = ProjectBanner
	template_name = 'project/banner.html'
	

	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)
		slug = self.kwargs['slug']
		
		college = self.request.user.user.college

			
		#banner = ProjectBanner.objects.get(slug=slug)
		banner = get_object_or_404(ProjectBanner , slug= slug)
		profile = banner.owner
		comments = Comment.objects.filter(
			projectsbanner__slug= banner.slug).prefetch_related('replies','user')


		

		context= {

			'profile':profile,
			'banner':banner,
			'comments': comments
		}

		return context 







class delete_banner(LoginRequiredMixin, UserPassesTestMixin ,DeleteView):
	model = ProjectBanner
	
	def get_success_url(self):
		slug = self.kwargs['slug']
		#banner = ProjectBanner.objects.get(slug=slug)
		banner = get_object_or_404(ProjectBanner , slug= slug)
		
		
		return reverse('user:home')

	def test_func(self):
		banner = self.get_object()
		user = self.request.user.user
		profile = get_object_or_404(Profile, slug = user.username)

		if banner.owner ==  profile :
			return True
		
		return False



@login_required
@update_project_permission
def update_project(request, slug):
	project = Project.objects.get(slug=slug)
	profile = Profile.objects.get(slug = project.author.slug)

	if request.method == 'POST':
		form =ProjectUpdationForm(request.POST , instance=project)

		if form.is_valid():
			form.save()
			form.instance.slug  =custom_slugify(form.instance.title, 
				allow_unicode=True)+'-'+str(form.instance.author.id)+str(form.instance.id)
			form.save()
			form.instance.tags.clear()
			data = form.cleaned_data['add_tags']
			for i in data.split('--')[:-1]:
				try:
					tag = Tag.objects.get(tag_name__iexact=i.strip())
				except:
					if i!=' ':
						tag = Tag.objects.create(tag_name=i.strip(),user_create=True)
						tag.save()
				form.instance.tags.add(tag)
		return redirect('project:detail-project', slug = form.instance.slug)
		
	else:
		form = ProjectUpdationForm(instance=project)

	
	context ={'form':form, 'profile': profile}

	return render(request,'project/updateproject.html',context)


class profile_projects(LoginRequiredMixin ,ListView):
	model = Project
	template_name = 'project/profileprojects.html'
	context_object_name= 'projects'
	paginate_by = 10

	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)
		slug = self.kwargs['slug']
		
		college = self.request.user.user.college

			
		profile = Profile.objects.get(slug=slug)
		total_projects = Project.objects.filter(author = profile).prefetch_related('tags','author')
		if profile.content_object.is_page():
			projects= total_projects.filter(Q(author__pages__college__name = college)|Q(visibility='PUBLIC')).order_by('-date_created')
		else:
			projects = total_projects.filter(Q(author__users__college__name = college)|Q(visibility='PUBLIC')).order_by('-date_created')
		
		paginated_projects = Paginator(projects,self.paginate_by)
		page_number = self.request.GET.get('page')
		projects = paginated_projects.get_page(page_number)
		
		

		context= {
			'projects': projects,
			'profile':profile,
		}

		return context 


class saved_projects(LoginRequiredMixin ,ListView):
	model = Saved
	template_name = 'project/savedprojects.html'
	paginate_by = 10

	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)
		
		profile = Profile.objects.get(slug=self.request.user.username)
		ct = ContentType.objects.get_for_model(Project)
		projects = profile.saved.filter(content_type=ct).prefetch_related(
			'content_object__tags', 'content_object__author')
		
		
		paginated_projects = Paginator(projects,self.paginate_by)
		page_number = self.request.GET.get('page')
		projects = paginated_projects.get_page(page_number)
		
		
		
		context= {
			'projects': projects,
		}

		return context 











class tag_projects(LoginRequiredMixin, ListView):
	model = Project
	template_name = 'project/tagprojects.html'
	context_object_name= 'projects'
	paginate_by = 10
	ordering =[ '-date_created']

	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)
		slug = self.kwargs['slug']
		
		college = self.request.user.user.college	
		tag = Tag.objects.get(slug=slug)
		projects = tag.project_set.all().prefetch_related('tags','author')
		
		total_projects = projects.filter(Q(visibility='PUBLIC')
			|Q(author__pages__college__name = college)
			|Q(author__users__college__name = college))
		
		
		paginated_projects = Paginator(total_projects,self.paginate_by,orphans=1)
		
		page_number = self.request.GET.get('page')
		
		try:
			projects = paginated_projects.get_page(page_number)
		except InvalidPage:
		 	print('this is InvalidPage')
		
		

		context= {
			'projects': projects,
			'tag' : tag,
		}

		return context 
	
