


''' ACTIVITY URLS '''
from django.urls import path

from . import views 


app_name = 'activity'

urlpatterns = [

	path('<slug:slug>/<str:object_type>/like/' ,views.like,  name = 'like-post' ),

	path('<slug:slug>/<object_type>/save/' ,views.save,  name = 'save-post-project' )

	]