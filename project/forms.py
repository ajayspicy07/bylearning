

''' PROJECT FORMS '''

from post.models import Tag
from .models import *
from django import forms
from tinymce.widgets import TinyMCE

from .models import *

class ProjectCreationForm(forms.ModelForm):
	add_tags = forms.CharField(widget=forms.TextInput())
	body = forms.CharField(widget=TinyMCE(attrs={'cols': 30, 'rows': 30}))
  

	class Meta:
		model = Project
		fields = (
	    	'title',
	    	'description',
	    	'body',
	        'add_tags',
	    	'comments',
	    	'visibility',
	    
	    	)

class ProjectUpdationForm(forms.ModelForm):
	add_tags = forms.CharField(widget=forms.TextInput())
	body = forms.CharField(widget=TinyMCE(attrs={'cols': 30, 'rows': 30}))

	class Meta:
		model = Project
		fields = (
	    	'title',
	    	'description',
	    	'body',
	        'add_tags',
	    	'comments',
	    	'visibility',
	    
	    	)


	def __init__(self,*args,**kwargs):
		super(ProjectUpdationForm,self).__init__(*args,**kwargs)
		tagstring=''
		for tags in self.instance.tags.all():
			tagstring+=tags.tag_name+'--'

		self.fields['add_tags'].widget.attrs['value']=tagstring
		
     

class BannerCreationForm(forms.ModelForm):

	class Meta :
		model = ProjectBanner
		fields =(
				'heading',
				'skills_required',
				'body',
			)

  


