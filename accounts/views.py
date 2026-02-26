from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm
from student.models import Student


def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)

        if form.is_valid():
            user = form.save()   
            user.role = 'student'
            user.save(update_fields=['role'])

            return redirect('login')

        else:
            print("ERRORS:", form.errors)

    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            if user.role == 'principal':
                return redirect('principal_dashboard')
            else:
                return redirect('student_dashboard')

    return render(request, 'accounts/login.html')


def user_logout(request):
    logout(request)
    return redirect('login')