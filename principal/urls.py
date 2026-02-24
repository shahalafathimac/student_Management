from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.principal_dashboard, name='principal_dashboard'),
    path('courses/', views.manage_courses, name='manage_courses'),
    path('courses/add/', views.add_course, name='add_course'),
    path('courses/delete/<int:pk>/', views.delete_course, name='delete_course'),
    path('users/', views.manage_users, name='manage_users'),
    path('approvals/', views.approvals, name='approvals'),
]