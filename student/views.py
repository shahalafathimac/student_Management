from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

# @login_required
def student_dashboard(request):
    return render(request, 'students/dashboard.html')


# @login_required
def my_courses(request):
    return render(request, 'students/my_courses.html')


# @login_required
def course_purchase(request):
    return render(request, 'students/purchase.html')


# @login_required
def profile(request):
    return render(request, 'students/profile.html')


# @login_required
def settings(request):
    return render(request, 'students/settings.html')

def logout_view(request):
    return render(request)