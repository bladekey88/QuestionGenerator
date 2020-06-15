"""question_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, include,re_path
from upload.views import SignUpView, ProfileView
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings
from . import views




urlpatterns = [
   
    # Upload App - e.g /upload
    path('upload/', include('upload.urls')),

    # API App - e.g /api
    path('api/', include('api.urls')),

    path('api-auth/', include('rest_framework.urls')),

    # Messages App e.g. /messages
    path('messages/', include('messaging.urls')),

    # Messages App e.g. /messages
    path('worksheet/', include('worksheet.urls')),
    
    


    # Admin App - /admin
    path('admin/', admin.site.urls),

    # User Authentication Functions /signup /login /logout /change-password
    path('register/', SignUpView.as_view(), name='register'),
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html', redirect_authenticated_user=True, ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='common/logout.html',next_page='home' ), name='logout'),
    path('change-password/', auth_views.PasswordChangeView.as_view(template_name='common/change-password.html', success_url = '/'), name='change-password'), 

    #Forget Password
    path('password-reset/',auth_views.PasswordResetView.as_view(
             template_name='common/password-reset/password-reset.html', 
             subject_template_name='common/password-reset/password-reset-subject.txt',
             email_template_name='common/password-reset/password-reset-email.html',
            #  success_url='/login/'
         ), name='password_reset'),
         
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='common/password-reset/password-reset-done.html'
         ),
         name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='common/password-reset/password-reset-confirm.html'
         ),
         name='password_reset_confirm'),
    
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='common/password-reset/password-reset-complete.html'
         ),
         name='password_reset_complete'),

    


    # example admin scheme
    path('django-sb-admin/', include('django_sb_admin.urls')),    
  
    
    # root directory (currently) /
    #path('', TemplateView.as_view(template_name='common/home.html'), name='home'),
    path('', views.home, name='home'),


       
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if not settings.DEBUG:
    handler400 = 'question_project.views.bad_request'
    handler403 = 'question_project.views.permission_denied'
    handler404 = 'question_project.views.page_not_found'
    handler500 = 'question_project.views.server_error'