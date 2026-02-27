from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    path('profile/', views.student_profile, name='student_profile'),
    path('purchase/', views.purchase_courses, name='purchase_courses'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('search/',       views.search_courses,      name='search_courses'),
]