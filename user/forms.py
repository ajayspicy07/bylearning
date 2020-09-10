

'''	 USER FORMS '''
from django.contrib.auth.forms import UserCreationForm
from django import forms

from django.db import models
from .models import *

class UserRegistrationForm(UserCreationForm):
	username = forms.CharField(widget=forms.TextInput(attrs={'id':'username','class':'box-input'}))
	first_name = forms.CharField(widget=forms.TextInput(attrs={'id':'first_name','class':'box-input'}))
	last_name = forms.CharField(widget=forms.TextInput(attrs={'id':'last_name','class':'box-input'}))
	email = forms.EmailField(widget=forms.TextInput(attrs={'id':'email','class':'box-input'}))
	dob = forms.DateTimeField(widget=forms.TextInput(attrs={'id':'dob','class':'box-input','type':'date'}))
	
	class Meta:
		model = User
		fields= (
	      'username',
	      'first_name',
	      'last_name',
	      'email',
	      'user_mode',
	      'college',
	      'dob',
	      'password1',
	      'password2',
	    )


class LoginForm(forms.ModelForm):
	username_email = forms.CharField()
	password = forms.CharField(widget= forms.PasswordInput)
	class Meta:
		model=User
		fields = ['username_email','password']

class ProfileUpdateForm(forms.ModelForm):
	description = forms.CharField(required=False, widget=forms.Textarea(attrs=
		{'placeholder':'Write your description here.. ',
		 'rows':4, 'cols':6 }))

	class Meta:
		model = Profile
		fields = ['image','description']



class UserUpdateForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['email']


class PageUpdateForm(forms.ModelForm):
	add_members = forms.CharField()

	class Meta:
		model = Page
		fields = ['name','add_members']

	def __init__(self,*args,**kwargs):
		super(PageUpdateForm, self).__init__(*args, **kwargs)
		self.fields['add_members'].required = False
	