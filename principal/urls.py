from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.principal_dashboard, name='principal_dashboard'),
]