"""flearn URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.urls import path,include


from django.conf.urls.static import static
from django.contrib.auth import views as  auth_views


from django.conf import settings
import user,post,project,comment,activity

admin.site.site_header = 'Flearn Admin'
admin.site.site_title = 'Flearn Admin'
admin.site.index_title = 'Flearn Admin'





urlpatterns = [
    path('special_admin/', admin.site.urls),

    path('tinymce/', include('tinymce.urls')),
  

    path('',include('user.urls')),
    path('',include('post.urls')),
    path('',include('project.urls')),
    path('',include('comment.urls')),
    path('',include('activity.urls')),


    path('password-reset/', 
        auth_views.PasswordResetView.as_view(template_name='password-reset.html'),
         name='password-reset'),
    path('password_reset_done/', 
        auth_views.PasswordResetDoneView.as_view(template_name='password-reset-done.html'),
         name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>',
        auth_views.PasswordResetConfirmView.as_view(template_name='password-reset-confirm.html'),
         name='password_reset_confirm'),
   
    
    path('password-reset-complete/',
        auth_views.PasswordResetCompleteView.as_view(template_name='password-reset-complete.html'),
         name='password_reset_complete'),
   
    path('login/', user.views.login, name = "login"),


]


urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ] 

