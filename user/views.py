
''' USER VIEWS  '''

from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse, Http404,HttpResponseRedirect

from slugify import UniqueSlugify,Slugify
from django.contrib import auth,messages
from django.views.generic import CreateView,ListView,DetailView

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required

import operator
from functools import reduce
from django.db.models import Q


from django.views.decorators.csrf import csrf_exempt

from .models import *
from post.models import Post,PostDirectory
from project.models import Project,ProjectBanner
from .forms import *
from .decorators import *

''' SOME LOGIC '''
custom_slugify = Slugify()

# Create your views here.
def index(request):
	return render(request,'user/index.html')

def about_us(request):
	return render(request,'user/aboutus.html')	

@login_required
def home(request):
	college = request.user.user.college
	banners = ProjectBanner.objects.filter(owner__users__college = college)
	context = {
		'banners' : banners
	}
	
	return render(request,'user/home.html', context)

@authenticated_user
def signup(request):
	if request.method=='POST':
		form = UserRegistrationForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			
			if  '.' in username or '@' in username or '_' in username or '--' in username or '-' == username[-1]:
				messages.error(request, 'Check Username?')
				pass
			else:
				form.save()
				username = form.cleaned_data['username']
				password = form.cleaned_data['password1']
				user = auth.authenticate(username=custom_slugify(username), password=password)
			
				auth.login(request,user)
				return redirect('user:profile', slug=username)
	else:
		form=UserRegistrationForm()
	return render(request,'user/signup.html',{'form':form})


def validate_username(request):
	username=request.GET.get('username',None)

	data = {
		'is_taken': User.objects.filter(username__iexact=username).exists()
	}
	
	if data['is_taken']:
		message='User with that username already exists'
	
	elif '.' in username or '@' in username or '_' in username or '--' in username or '-' == username[-1]:
		message = 'Invalid Username'
	
	else:
		message='Username is available'
		
	return JsonResponse(message,safe=False)

@authenticated_user
def login(request):
	form = LoginForm()
	if request.method == 'POST':
		name = request.POST['username_email'].strip()
		password = request.POST['password']
		
		try :
			
			user = auth.authenticate(username=User.objects.get(email__iexact=name).username, password= password)
		except:
			user = auth.authenticate(username=name, password=password)
		
		if user is not None:
			auth.login(request,user)
			if request.GET.get('next',None):
				return HttpResponseRedirect(request.GET['next'])
			return redirect('user:home')
		else:
			if User.objects.filter(email=name).exists() or User.objects.filter(username=name).exists():
				messages.error(request, 'Username or password is Wrong?')
			else:
				messages.error(request, "Account with that Email or Username doesn't exist")
		

	return render(request,'user/login.html', context={'form':form})


class create_page(LoginRequiredMixin,CreateView):
	model = Page
	fields = ['name']
	template_name = 'user/createpage.html'

	def form_valid(self, form):
		form.instance.admin = self.request.user.user
		form.instance.college = self.request.user.user.college
		return super().form_valid(form)


@login_required
def profile(request,slug):
	profile=Profile.objects.get(slug=slug)
	college = request.user.user.college
	requested_profile = Profile.objects.get(users__username=request.user.username)
	if Follower.objects.filter(from_profile=requested_profile,to_profile=profile).exists():
		is_followed= True
	else:
		is_followed= False

	posts = profile.posts.filter(Q(author__users__college__name = college)
		|Q(visibility='PUBLIC')|Q(author__pages__college__name=college))[:5]

	projects = profile.projects.filter(Q(author__users__college__name = college)
		|Q(visibility='PUBLIC')|Q(author__pages__college__name=college))[:5]

	folders = profile.folders.filter(Q(owner__users__college=college)
		|Q(visibility = 'PUBLIC')|Q(owner__pages__college__name=college))[:5]

	if profile.content_object.is_page():
		members = profile.content_object.members.all()
		if User.objects.get(username=request.user.username) in members :
			is_member = True
		else:
			is_member= False
		context = {'profile':profile,'members': members,
				 'is_member':is_member,'is_followed':is_followed,
				 'posts':posts, 'projects':projects, 'folders':folders
				 }
	else:
		user = request.user.user
		member_pages = user.page_members.all()
		values_list =[]
		for i  in member_pages:
			values_list.append(i.id)

		
		admin_pages_profiles = Profile.objects.filter(pages__admin=user)
		
		ct = ContentType.objects.get_for_model(Page)
		member_pages_profiles = Profile.objects.filter(content_type=ct, object_id__in = values_list)
		
		pages = admin_pages_profiles|member_pages_profiles

		context = {'profile':profile, 'is_followed':is_followed,
				 'posts':posts, 'projects':projects, 'folders':folders,
				 'pages':pages
				 }

	return render(request,'user/profile.html', context)


@login_required
@update_profile_permission
def update_profile(request, slug):
	profile = Profile.objects.get(slug=slug)
	if request.method == 'POST':
		profile_form =ProfileUpdateForm(request.POST ,request.FILES, instance=profile)
	
		if profile.content_object.is_page() :
			
			unique_form = PageUpdateForm(request.POST,
				instance=Page.objects.get(name=profile.content_object))
		else:
			
			unique_form = UserUpdateForm(request.POST,
				instance = User.objects.get(username=profile.content_object.username))
		
		 
		if profile_form.is_valid() and unique_form.is_valid():
			
			profile_form.save()
			
			if profile.content_object.is_page():
				members = unique_form.cleaned_data['add_members']
				page_name = unique_form.cleaned_data['name']
     
				unique_form.save()
				unique_form.instance.members.clear()
				for member in members.split('--')[:-1]:
					user = User.objects.get(username__iexact=member)
					unique_form.instance.members.add(user.id)
				profile.slug= custom_slugify(page_name)+'-'+str(unique_form.instance.id)

			unique_form.save()

			return redirect('user:profile',slug=profile.slug)
		
	else:
		profile_form = ProfileUpdateForm(instance=profile)
		if profile.content_object.is_page() :
			unique_form = PageUpdateForm(instance=Page.objects.get(name=profile.content_object))
		else:
			unique_form = UserUpdateForm(instance=User.objects.get(username=profile.content_object.username))


	
	context ={'profile_form':profile_form,'unique_form':unique_form , 'profile':profile}

	return render(request,'user/updateprofile.html',context)

def add_member(request):

	username=request.GET.get('username',None)
	
	if User.objects.filter(username__iexact=username).exists():
		profile = Profile.objects.get(users__username__iexact=username)
		profile_data={
			'name': str(profile),
			'image' : profile.image.url,
			'username': profile.content_object.username
		}
	else:
		profile_data=[]


	return JsonResponse(profile_data,safe=False)


@csrf_exempt
@login_required
def follow_profile(request,slug):
	to_user= Profile.objects.filter(slug=slug).first()
	
	from_user=Profile.objects.filter(users__username=request.user).first()
	if request.method == 'POST':
		if Follower.objects.filter(from_profile=from_user,to_profile=to_user).exists():
			Follower.objects.filter(from_profile=from_user,to_profile=to_user).delete()
			message = 'Deleted'

		
		else:
			Follower.objects.create(from_profile=from_user,to_profile=to_user)
			message = 'Created'

	return JsonResponse(message,safe=False)

@login_required
def get_followers(request,slug):
	
	profile = Profile.objects.get(slug=slug)
	
	followers_profiles = list(profile.following.all().values())
	profile_list=[]
	for i in range(len(followers_profiles)):
		individual_profile = Profile.objects.get(id = followers_profiles[i]['from_profile_id'])
		profile_values =  {
						'name': str(individual_profile), 
						'image': individual_profile.image.url,
						'slug':individual_profile.slug
		 				}
		profile_list.append(profile_values)

	
	return JsonResponse(profile_list,safe=False)

@login_required
def show_following_profiles(request):
	profile = Profile.objects.get(users__username=request.user)
	following_members = list(profile.followers.all().values())
	profile_list=[]
	for i in range(len(following_members)):
		individual_profile = Profile.objects.get(id = following_members[i]['to_profile_id'])
		profile_values =  {
						'name': str(individual_profile), 
						'image': individual_profile.image.url,
						'slug':individual_profile.slug
		 				}
		profile_list.append(profile_values)


	return JsonResponse(profile_list,safe=False)

@login_required
def search_post_projects(request):
	college = request.user.user.college
	search_list = request.GET.get('title',None)
	if search_list == '':
		search_list= ' '
	query = reduce(operator.and_ , (Q(title__icontains = item) for item in search_list))

	
	posts =  Post.objects.filter(query).filter(Q(author__users__college__name = college)
		|Q(visibility='PUBLIC')|Q(author__pages__college__name=college))[:10]
		
	projects = Project.objects.filter(query).filter(Q(author__users__college__name = college)
					|Q(visibility='PUBLIC')|Q(author__pages__college__name=college))[:10]
	
	
	

	context = {
		'posts': posts,
		'projects': projects
	}

	return render(request, 'user/searchresults.html' ,context)
		
