from django.shortcuts import render
from django.urls import path

from . import views 

app_name = 'account'

urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('email-verification-sent/', 
         lambda request:render(request, 'account/email/email-verification-sent.html'),
           name='email-verification-sent'),
    path('dashboard/', views.dashboard_user, name='dashboard'),    
    path('profile-manager', views.profile_user, name='profile-manager'),
    path('delete-user', views.delete_user, name='delete-user'),
]