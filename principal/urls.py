from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.principal_dashboard, name='principal_dashboard'),
    path('manage-courses/', views.manage_courses, name='manage_courses'),
    path('courses/<int:pk>/edit/',  views.edit_course,   name='edit_course'),
    path('courses/<int:pk>/delete/', views.delete_course, name='delete_course'),
    path('manage-students/', views.manage_students, name='manage_students'),
    path('students/<int:pk>/',views.view_student, name='view_student'),   
    path('students/<int:pk>/edit/',views.edit_student,name='edit_student'), 
    path('course-approvals/', views.course_approvals, name='course_approvals'),

]