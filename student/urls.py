from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    path('my-courses/', views.my_courses, name='my_courses'),
    path('course-purchase/', views.course_purchase, name='course_purchase'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout_view, name='logout'),
]