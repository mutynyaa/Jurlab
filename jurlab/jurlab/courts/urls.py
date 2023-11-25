from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path ('', views.court, name='court'),
    path('<int:pk>/', views.courts_detail, name='courts_detail'),
    path('new/', views.courts_new, name='courts_new'),
    path('new/step_one/<int:pk>', views.court_new_step_two, name='court_new_step_two'),
    path('<int:pk>/edit/', views.courts_edit, name='courts_edit'),
    path('arhive/', views.courts_arhive, name='courts_arhive'),
    path('<int:pk>/delete/', views.courts_delete, name='courts_delete'),
    path('courts_comments_delete/<int:pk>/', views.courts_comments_delete, name='courts_comments_delete'),
    path('courts_documents_delete/<int:pk>/', views.courts_documents_delete, name='courts_documents_delete'),
    path('courts_judgment_delete/<int:pk>/', views.courts_judgment_delete, name='courts_judgment_delete'),
    path('error_court/', views.error_court, name='error_court'),
]
