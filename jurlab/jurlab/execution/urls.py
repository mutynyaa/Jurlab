from django.contrib import admin
from django.urls import path, include
from . import views



urlpatterns = [
    path ('', views.executions, name='executions'),
    path('<int:pk>/', views.execution_details, name='execution_details'),
    path('new/<int:pk>/', views.execution_new, name='execution_new'),
    path('edit/<int:pk>', views.execution_edit, name='execution_edit'),
    path('arhive/', views.ex_arhive, name='ex_arhive'),
    path('ex_comments_delete/<int:pk>/', views.ex_comments_delete, name='ex_comments_delete'),
    path('<int:pk>/delete/', views.ex_delete, name='ex_delete'),
    path('ex_documents_delete/<int:pk>/', views.ex_documents_delete, name='ex_documents_delete'),
]