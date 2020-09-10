




''' POST MODELS '''

from django.db import models
from django.utils import timezone
from django.utils.text import slugify as inbuilt_slugify
from django.contrib.contenttypes.fields import GenericForeignKey,GenericRelation
from django.urls import reverse
from slugify import UniqueSlugify,Slugify
from tinymce.models import HTMLField


from user.models import *
#from comment.models import Comment


''' some logic '''
custom_slugify = Slugify()

# Create your models here.




''' Tags List '''
class Tag(models.Model):
	tag_name    =models.CharField(max_length=100)
	user_create =models.BooleanField(default=False)
	slug        =models.SlugField(max_length=100,blank=True)
	

	class Meta:
		db_table = "Tags"
  
  
	def __str__(self):
		return self.tag_name
		
	def save(self, *args, **kwargs):
		self.slug=custom_slugify(self.tag_name, allow_unicode=True)
		super().save(*args, **kwargs)


''' Base Post Model '''
class BasePost(models.Model):
	VISIBILITY = [
		
		('PRIVATE', 'My College Only' ),
		('PUBLIC', 'Public' ),
	]
	COMMENTS = [
		('ENABLE', 'Enable' ),
		('DISABLE', 'Disable' ),
	]
	
  
  
	title       =models.CharField(max_length=400)
	slug        =models.SlugField(max_length=400,unique=True,blank=True)
	description =models.TextField()

	body       = HTMLField()
	tags        =models.ManyToManyField(Tag , blank=True)
	likes       =models.PositiveIntegerField(default=0)
	views       =models.PositiveIntegerField(default=0)

	comments    =models.CharField(max_length=10, choices=COMMENTS ,default='ENABLE')
	visibility  =models.CharField(max_length=10, choices=VISIBILITY ,default='PRIVATE')
	
	date_created = models.DateTimeField(default=timezone.now) 
	last_modified = models.DateTimeField( auto_now=True)

	class Meta:
		abstract = True
	def __str__(self):
		return self.title
	'''
	def save(self, *args, **kwargs):
		self.slug=custom_slugify(self.title, allow_unicode=True)
		super().save(*args, **kwargs)
    
    '''
    
''' Base Folder '''
class BaseFolder(models.Model):
	VISIBILITY = [
		('PUBLIC', 'Public' ),
		('PRIVATE', 'My College Only' ),
	]

	name = models.CharField(max_length=1000)
	visibility  =models.CharField(max_length=10, choices=VISIBILITY ,default='PRIVATE')
	
	slug = models.SlugField(max_length=400,unique=True,blank=True)
	date_created = models.DateTimeField(default=timezone.now) 


	class Meta:
		abstract = True

	def __str__(self):
		return self.name

	'''
	def save(self, *args, **kwargs):
		self.slug=custom_slugify(self.name, allow_unicode=True)+'-'+str(self.id)
		super().save(*args, **kwargs)
   	'''
    
    
    
    
''' Post Model '''
class Post(BasePost):
	author      =models.ForeignKey(Profile,on_delete =models.CASCADE, related_name ="posts")
	comment_model =	 GenericRelation('comment.Comment', related_query_name='posts')
	liked		= GenericRelation('activity.Like', related_query_name='postlikes')
	saved= GenericRelation('activity.Saved', related_query_name='postsaved')

	class Meta:
		db_table = "Posts"
		ordering = ('-date_created',)


	def get_absolute_url(self):
		return reverse('post:detail-post', kwargs = {'slug':self.slug})
	#get reverse to user:index any problem if?


  
''' Post directory '''
class PostDirectory(BaseFolder):
	owner = models.ForeignKey(Profile,on_delete=models.CASCADE, related_name='folders')
	directory = models.ManyToManyField(Post,blank=True,)

	class Meta:
		db_table = "Post_Folders"
		ordering = ('-date_created',)
  
    
    
    
    