

''' Post VIEWS '''

from django.shortcuts import render, redirect
from django.http import HttpResponse,JsonResponse
from django.urls import reverse

from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404


from django.utils import timezone
from datetime import timedelta
from django.views.generic import CreateView,ListView,DetailView,UpdateView, DeleteView
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from slugify import UniqueSlugify,Slugify

#from django_filters.views import FilterView

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
def create_post(request, slug):
	profile = Profile.objects.get(slug=slug)
	if request.method == 'POST':
		form =PostCreationForm(request.POST)
		
		if form.is_valid():
			form.instance.author = profile
			form.save()
			form.instance.slug  =custom_slugify(form.instance.title, 
				allow_unicode=True)+'-'+str(profile.id)+str(form.instance.id)
			form.save()

			data = form.cleaned_data['add_tags']
			for i in data.split('--')[:-1]:
				try:
					tag = Tag.objects.get(tag_name__iexact=i)
				except:
					if i!=' ':
						tag = Tag.objects.create(tag_name=i,user_create=True)
						tag.save()
				form.instance.tags.add(tag)
			return redirect('post:detail-post', slug = form.instance.slug)
		
	else:
		form =PostCreationForm(request.POST)
	
	context ={'form':form, 'profile':profile}
	return render(request,'post/createpost.html',context)


def tagautocomplete(request):
	if 'term' in request.GET:
		qs = Tag.objects.filter(tag_name__icontains=request.GET.get('term'))[:10]
		tags = []
		for tag in qs:
			tags.append(tag.tag_name)
		
		return JsonResponse(tags,safe=False)


class posts(LoginRequiredMixin, ListView):
	model = Post
	template_name = 'post/posts.html'
	paginate_by = 5
	ordering =[ '-date_created']

	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)
		college = self.request.user.user.college

		context['filter']= PostFilter(self.request.GET, 
			queryset=self.get_queryset().filter(Q(
				author__users__college__name = college)|Q(
				visibility='PUBLIC')|Q(author__pages__college__name=college)),
			user=self.request.user )

		paginated_filterd_posts = Paginator(context['filter'].qs,self.paginate_by)
		page_number = self.request.GET.get('page')
		posts_per_page = paginated_filterd_posts.get_page(page_number)
		context['posts_per_page'] = posts_per_page
		return context



 


	
class detail_post(LoginRequiredMixin, DetailView):
	model = Post
	template_name= 'post/postdetail.html'
	

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
		
		
		post = get_object_or_404(Post, slug=slug)
		key=post.slug
		session = self.request.session.get(key)
		if post.visibility == 'PUBLIC' or post.author.content_object.college == college:
			if self.request.user.is_authenticated and self.get_ip() and not session:
				post.views+=1
				post.save()
				self.request.session[key]=True
		comments = Comment.objects.filter(posts__slug= post.slug)
		context={
			'post':post,
			'comments': comments,
		}


		return context
 


		

	'''
	def test_func(self):
		post = self.get_object()
		college = self.request.user.user.college
		if post.visibility == 'PUBLIC' or post.author.content_object.college == college:
			return True
		else:
			return False

	'''
class delete_post(LoginRequiredMixin,UserPassesTestMixin, DeleteView):
	model = Post
	
	def get_success_url(self):
		slug = self.kwargs['slug']
		author = Post.objects.get(slug=slug).author.slug
		return reverse('post:profile-posts', kwargs= {'slug':author})

	def test_func(self):
		post = self.get_object()
		user = self.request.user.user
		profile = get_object_or_404(Profile, slug = user.username)

		if post.author.content_object.is_page():
			if user in post.author.content_object.members.all() or user == post.author.content_object.admin:
				return True
		else:
			if profile == post.author:
				return True
		return False





@login_required
@permission
def create_folder(request, slug):
	profile = Profile.objects.get(slug=slug)
	if request.method == 'POST':
		form =FolderCreationForm(request.POST)
		
		if form.is_valid():
			form.instance.owner = profile

			form.save()
			form.instance.slug  =custom_slugify(form.instance.name, 
				allow_unicode=True)+'-'+str(profile.id)+str(form.instance.id)
			form.save()
			return redirect('post:folder', slug = form.instance.slug )
		
	else:
		form =FolderCreationForm(request.POST)
	
	context ={'form':form, 'profile':profile}
	return render(request,'post/createfolder.html',context)



class folder(LoginRequiredMixin,ListView):
	model = PostDirectory
	template_name = 'post/folder.html'
	paginate_by = 2
	ordering =[ '-date_created']

	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)
		slug = self.kwargs['slug']
		
		college = self.request.user.user.college

			
		folder = PostDirectory.objects.get(slug=slug)
		profile = folder.owner

		posts = folder.directory.all()
		

		context= {
			'posts': posts,
			'profile':profile,
			'folder':folder,
		}

		return context 



@login_required
@folder_post_permission
def create_post_for_folder(request, slug):
	folder = PostDirectory.objects.get(slug=slug)
	profile = folder.owner
	if request.method == 'POST':
		form =PostCreationForm(request.POST)
		
		if form.is_valid():
			form.instance.author = profile
			form.save()
			form.instance.slug  =custom_slugify(form.instance.title, 
				allow_unicode=True)+'-'+str(profile.id)+str(form.instance.id)
			form.save()

			data = form.cleaned_data['add_tags']
			for i in data.split('--')[:-1]:
				try:
					tag = Tag.objects.get(tag_name__iexact=i)
				except:
					if i!=' ':
						tag = Tag.objects.create(tag_name=i,user_create=True)
						tag.save()
				form.instance.tags.add(tag)
			folder.directory.add(form.instance)
			return redirect('post:folder', slug = folder.slug)
		
	else:
		form =PostCreationForm(request.POST)
	
	context ={'form':form, 'profile':profile}
	return render(request,'post/createpost.html',context)





class delete_folder(LoginRequiredMixin , UserPassesTestMixin,DeleteView):
	model = PostDirectory
	
	def get_success_url(self):
		slug = self.kwargs['slug']
		folder = PostDirectory.objects.get(slug=slug)
		profile = folder.owner
		return reverse('post:profile-folders' , kwargs= {'slug': profile.slug })

	def test_func(self):
		folder = self.get_object()
		user = self.request.user.user
		profile = get_object_or_404(Profile, slug = user.username)

		if folder.owner.content_object.is_page():
			if user in folder.owner.content_object.members.all() or user == folder.owner.content_object.admin :
				return True
		else:
			if profile == folder.owner:
				return True
		return False




@login_required
@update_post_permission
def update_post(request, slug):
	post = Post.objects.get(slug=slug)
	profile = Profile.objects.get(slug = post.author.slug)

	if request.method == 'POST':
		form =PostUpdationForm(request.POST , instance=post)

		if form.is_valid():
			form.save()
			form.instance.slug  =custom_slugify(form.instance.title, 
				allow_unicode=True)+'-'+str(form.instance.author.id)+str(form.instance.id)
			form.save()
			form.instance.tags.clear()
			data = form.cleaned_data['add_tags']
			for i in data.split('--')[:-1]:
				try:
					tag = Tag.objects.get(tag_name__iexact=i)
				except:
					if i!=' ':
						tag = Tag.objects.create(tag_name=i,user_create=True)
						tag.save()
				form.instance.tags.add(tag)
		return redirect('post:detail-post', slug = form.instance.slug)
		
	else:
		form = PostUpdationForm(instance=post)

	
	context ={'form':form, 'profile': profile}

	return render(request,'post/updatepost.html',context)


class profile_posts(LoginRequiredMixin ,ListView):
	model = Post
	template_name = 'post/profileposts.html'
	context_object_name= 'posts'
	paginate_by = 5

	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)
		slug = self.kwargs['slug']
		
		college = self.request.user.user.college

			
		profile = Profile.objects.get(slug=slug)
		total_posts = Post.objects.filter(author = profile)
		if profile.content_object.is_page():
			posts= total_posts.filter(Q(author__pages__college__name = college)|Q(visibility='PUBLIC')).order_by('-date_created')
		else:
			posts = total_posts.filter(Q(author__users__college__name = college)|Q(visibility='PUBLIC')).order_by('-date_created')
		
		paginated_posts = Paginator(posts,self.paginate_by)
		page_number = self.request.GET.get('page')
		posts = paginated_posts.get_page(page_number)
		
		

		context= {
			'posts': posts,
			'profile':profile,
		}

		return context 



class saved_posts(LoginRequiredMixin ,ListView):
	model = Saved
	template_name = 'post/savedposts.html'
	paginate_by = 2

	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)
		
		profile = Profile.objects.get(slug=self.request.user.username)
		ct = ContentType.objects.get_for_model(Post)
		posts = profile.saved.filter(content_type=ct)
		
		
		paginated_posts = Paginator(posts,self.paginate_by)
		page_number = self.request.GET.get('page')
		posts = paginated_posts.get_page(page_number)
		
		
		
		context= {
			'posts': posts,
		}

		return context 




















class profile_folders(LoginRequiredMixin, ListView):
	model = PostDirectory
	template_name = 'post/profilefolders.html'
	context_object_name= 'posts'
	paginate_by = 1
	

	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)
		slug = self.kwargs['slug']
		
		college = self.request.user.user.college

			
		profile = Profile.objects.get(slug=slug)
		folders = PostDirectory.objects.filter(owner = profile)
		if profile.content_object.is_page():
			folders= folders.filter(Q(owner__pages__college__name = college)
				|Q(visibility='PUBLIC')).order_by('-date_created')
		else:
			folders = folders.filter(Q(owner__users__college__name = college)
				|Q(visibility='PUBLIC')).order_by('-date_created')
		
		context= {
			'folders': folders,
			'profile':profile,
		}

		return context 




class tag_posts(LoginRequiredMixin, ListView):
	model = Post
	template_name = 'post/tagposts.html'
	context_object_name= 'posts'
	paginate_by = 4
	ordering =[ '-date_created']

	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)
		slug = self.kwargs['slug']
		
		college = self.request.user.user.college

			
		tag = Tag.objects.filter(slug=slug).first()
		total_posts = tag.post_set.all().filter(Q(visibility='PUBLIC')
			|Q(author__pages__college__name = college)
			|Q(author__users__college__name = college))
		paginated_posts = Paginator(total_posts,self.paginate_by)
		page_number = self.request.GET.get('page')
		posts = paginated_posts.get_page(page_number)
		
		

		context= {
			'posts': posts,
			'tag' : tag,
		}
		
		return context 
	
