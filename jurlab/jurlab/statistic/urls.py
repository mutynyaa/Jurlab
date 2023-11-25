from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path ('', views.all_statistic, name='all_statistic'),
    path ('personal_statistic/', views.personal_statistic, name='personal_statistic'),
    path ('users_statistic/', views.users_statistic, name='users_statistic'),
]
