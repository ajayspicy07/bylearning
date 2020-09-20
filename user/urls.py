


''' USER URLS '''


from django.urls import path
from django.contrib.auth import views as  auth_views


#from . import views
from . import views 

app_name = 'user'

urlpatterns = [
    path('', views.index, name = "index"),
    path('home/' , views.home , name = "home"),
    path('about-us/', views.about_us, name = "about-us"),

    path('signup/', views.signup, name = "signup"),
    path('validate-username/', views.validate_username, name="validate-username"),
    path('login/', views.login, name = "login"),

    path('search/', views.search_post_projects, name = 'search-post-project'),

   
    path('p/<slug:slug>/', views.profile, name= "profile"),
    path('p/<slug:slug>/update-profile', views.update_profile, name= "update-profile"),

    path('createpage/', views.create_page.as_view(), name = "create-page"),
    path('add-member/' , views.add_member, name="add-member"),

    path('follow/<slug:slug>/', views.follow_profile, name='follow-profile'),
    path('get-followers/<slug:slug>/', views.get_followers, name='get-followers'),
    path('show-following-profiles/', views.show_following_profiles, name='show-following-profiles'),
    
    path('logout/', auth_views.LogoutView.as_view(template_name='user/index.html'), name='logout'),
   
    

]
