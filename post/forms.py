

''' POST FORMS '''
from .models import Post,Tag
from django import forms
from tinymce.widgets import TinyMCE

from .models import *

class PostCreationForm(forms.ModelForm):
	add_tags = forms.CharField(widget=forms.TextInput())
	body = forms.CharField(widget=TinyMCE(attrs={'cols': 30, 'rows': 30}))
  

	class Meta:
		model = Post
		fields = (
	    	'title',
	    	'description',
	    	'body',
	        'add_tags',
	    	'comments',
	    	'visibility',
	    
	    	)

class PostUpdationForm(forms.ModelForm):
	add_tags = forms.CharField(widget=forms.TextInput())
	body = forms.CharField(widget=TinyMCE(attrs={'cols': 30, 'rows': 30}))

	class Meta:
		model = Post
		fields = (
	    	'title',
	    	'description',
	    	'body',
	        'add_tags',
	    	'comments',
	    	'visibility',
	    	
	    	)


	def __init__(self,*args,**kwargs):
		super(PostUpdationForm,self).__init__(*args,**kwargs)
		tagstring=''
		for tags in self.instance.tags.all():
			tagstring+=tags.tag_name+'--'

		self.fields['add_tags'].widget.attrs['value']=tagstring
		
     

class FolderCreationForm(forms.ModelForm):

	class Meta :
		model = PostDirectory
		fields =(
				'name',
				'visibility',
			)

  


