from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Profile


# HOME PAGE
def home(request):
    return render(request, 'accounts/home.html')


# REGISTER
def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        role = request.POST.get("role")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("home")

        user = User.objects.create_user(
            username=username,
            password=password
        )

        Profile.objects.create(
            user=user,
            role=role
        )

        login(request, user)

        if role == "student":
            return redirect("student_dashboard")
        elif role == "principal":
            return redirect("principal_dashboard")

    return redirect("home")


# LOGIN
def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            role = user.profile.role

            if role == "student":
                return redirect("student_dashboard")
            elif role == "principal":
                return redirect("principal_dashboard")

        else:
            messages.error(request, "Invalid credentials")

    return redirect("home")


# LOGOUT
def user_logout(request):
    logout(request)
    return redirect("home")