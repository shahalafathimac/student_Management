from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from accounts.models import Profile
from .models import Course


# 🔒 Principal Role Check
def principal_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('home')

        if request.user.profile.role != "principal":
            return redirect('home')

        return view_func(request, *args, **kwargs)
    return wrapper


# DASHBOARD
@login_required
@principal_required
def principal_dashboard(request):
    total_courses = Course.objects.count()
    total_users = User.objects.count()

    context = {
        'total_courses': total_courses,
        'total_users': total_users,
    }

    return render(request, 'principal/dashboard.html', context)


# MANAGE COURSES
@login_required
@principal_required
def manage_courses(request):
    courses = Course.objects.all()
    return render(request, 'principal/manage_courses.html', {'courses': courses})


# ADD COURSE
@login_required
@principal_required
def add_course(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        price = request.POST.get("price")

        Course.objects.create(
            title=title,
            description=description,
            price=price
        )

        return redirect('manage_courses')

    return render(request, 'principal/add_course.html')


# DELETE COURSE
@login_required
@principal_required
def delete_course(request, pk):
    course = Course.objects.get(id=pk)
    course.delete()
    return redirect('manage_courses')


# MANAGE USERS
@login_required
@principal_required
def manage_users(request):
    users = User.objects.all()
    return render(request, 'principal/manage_users.html', {'users': users})


# APPROVALS (dummy for now)
@login_required
@principal_required
def approvals(request):
    return render(request, 'principal/approvals.html')