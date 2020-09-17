

''' USER MODEL '''

from django.db import models
from django.utils.text import slugify as inbuilt_slugify

from django.contrib.auth.models import User as auth_user
from django.utils import timezone
from slugify import UniqueSlugify,Slugify
from PIL import Image
from django.conf import settings

from django.urls import reverse
#from django.shortcuts import redirect

from django.contrib.contenttypes.fields import GenericForeignKey,GenericRelation
from django.contrib.contenttypes.models import ContentType

''' some logic '''
#custom_slugify = UniqueSlugify()

custom_slugify=Slugify()



# Create your models here.

''' College list '''
class College(models.Model):
	name    =models.CharField(max_length=200)
	district=models.CharField(max_length=100)
	state   =models.CharField(max_length=100)

	class Meta:
		db_table = "Colleges"
		ordering = ('name',)

	def __str__(self):
		return self.name

''' User MOdel '''
class User(auth_user):

	TYPE =[
	('STUDENT','Student'),
	('EDUCATOR','Proffesor/Teacher/Educator')
	]

	college     = models.ForeignKey(College,on_delete=models.SET_NULL,null=True)

	dob         = models.DateField(blank=False)
	user_mode   = models.CharField(max_length=10, choices=TYPE, default ='STUDENT')
	date_created  = models.DateTimeField(auto_now_add=True, blank=False)
	profile      = GenericRelation('Profile', related_query_name='users')


	class Meta:
		db_table = "Users"

	@property
	def is_page(self):
		return False
	



	def full_name(self):
		return self.first_name+' ' +self.last_name

	def profile_name(self):
		return self.username

	def is_page(self):
		return False

	def __str__(self):
		return self.first_name+' ' +self.last_name


  


class Page(models.Model):
	name        =models.CharField(max_length=600)
	admin       =models.ForeignKey(User, on_delete=models.CASCADE,related_name='page_admin')
	members     =models.ManyToManyField( User, blank=True, related_name= 'page_members' )
	college     =models.ForeignKey(College,on_delete=models.CASCADE, blank= True)
	date_created=models.DateTimeField(auto_now_add=True, blank=False) 
	profile     = GenericRelation('Profile', related_query_name='pages') 

	class Meta:
		db_table= "Pages"

	@property
	def is_page(self):
		return True
	


	def full_name(self):
		return self.name


	def profile_name(self):
		return self.name

	def is_page(self):
		return True

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		profile = Profile.objects.get(pages__name = self.name, pages__admin = self.admin )
		return reverse('user:profile' ,kwargs={'slug': profile.slug})

class Profile(models.Model):

	limit = models.Q(model='user') | models.Q(model ='page')
	content_type = models.ForeignKey(
	    ContentType, on_delete=models.CASCADE,
	    limit_choices_to=limit, blank=False,
	)
	object_id = models.PositiveIntegerField(blank=True, null =False)
	content_object = GenericForeignKey('content_type', 'object_id')
	slug =models.SlugField(blank=True,unique=True)
	image = models.ImageField( default='profile_pics/default.png',upload_to='profile_pics')
	description = models.TextField(blank=True)

	class Meta:
		db_table = "Profiles"

	@property
	def college(self):
		return str(self.content_object.college)

	def __str__(self):
		return self.content_object.full_name()

		
	def save(self, *args, **kwargs):
		if self.content_object.is_page():
			self.slug=custom_slugify(self.content_object.profile_name(), 
				allow_unicode=True)+'-'+str(self.content_object.id)
		else:

			self.slug=custom_slugify(self.content_object.profile_name(), 
				allow_unicode=True)

		super().save(*args, **kwargs)

		if settings.DEBUG :
			img = Image.open(self.image.path)

			if img.height > 300 or img.width > 300:
				output_size = (300, 300)
				img.thumbnail(output_size)
				img.save(self.image.path)

		
		
		
		'''
		
		img = Image.open(self.image.path)
		#img = Image.open(self.image.file)
		if img.height > 300 or img.width > 300:
			output_size = (300, 300)
			img.thumbnail(output_size)
			img.save(self.image.path)
			#img.save(self.image.file)
			
			#img.save(self.image.path)
			
			#img.save(self.img.file)
			#img.save(tempimg,'image/jpeg')
			#self.image.save(img)
		'''
		
		
    
		
		
		
	def college(self):
		return str(self.content_object.college)

class Follower(models.Model):
	from_profile =models.ForeignKey(Profile,on_delete=models.CASCADE,
		related_name='followers')
	to_profile   =models.ForeignKey(Profile,on_delete=models.CASCADE, 
		related_name='following')
	date_created =models.DateTimeField(auto_now_add=True)

	class Meta:
		db_table = "Follower"

	def __str__(self):
		return str(self.from_profile) +' follow '+ str(self.to_profile)

	
     
  
  
  

	
	

	

