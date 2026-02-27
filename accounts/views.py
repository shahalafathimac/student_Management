from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm
from student.models import Student
from django.core.mail import send_mail
from django.conf import settings


def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)

        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'student'
            user.save()

             # Send welcome email
            try:
                send_mail(
                    subject='Welcome to Student Management System',
                    message=f"""Hello {user.first_name or user.username},
                    Your account has been successfully created.
                    Login here: http://127.0.0.1:8000/accounts/login/
                    Username : {user.username}
                    Thank you!
                    Team StudentMS""",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    fail_silently=False,
                )
            except Exception as e:
                print(f"Email failed: {e}")  # don't break registration if email fails

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