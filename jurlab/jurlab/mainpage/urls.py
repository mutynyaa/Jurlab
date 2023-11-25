from django.contrib import admin
from django.urls import path, include
from . import views
from .views import JurlabLoginView


urlpatterns = [
    path ('', views.mainpage, name='mainpage'),
    path ('supervisor/', views.supervisor, name='supervisor'),
    path('login', views.JurlabLoginView.as_view(), name='login_page'),
    path('logout', views.JurlabLogout.as_view(), name='logout_page'),
    path ('clear_uncomplete_courts/', views.clear_uncomplete_courts, name='clear_uncomplete_courts'),
]

