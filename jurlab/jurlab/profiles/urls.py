from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path ('', views.profiles, name='profiles'),
    path ('myprofile/', views.myprofile, name='myprofile'),
    path ('<int:pk>/', views.profile_detail, name='profile_detail'),
]