from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm
from student.models import Student
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import get_user_model


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


User = get_user_model()

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()

        try:
            user = User.objects.get(email=email)
            uid   = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

            reset_link = request.build_absolute_uri(
                f'/reset-password/{uid}/{token}/'   
            )

            try:
                send_mail(
                    subject='Password Reset Request - StudentMS',
                    message=f"""Hello {user.first_name or user.username},

We received a request to reset your password.

Click the link below to set a new password:
{reset_link}

This link expires in 24 hours. If you didn't request this, ignore this email.

Team StudentMS""",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                    fail_silently=False,
                )
            except Exception as e:
                print(f"Email failed: {e}")

        except User.DoesNotExist:
            pass

        return render(request, 'accounts/forgot_password.html', {
            'sent': True
        })

    return render(request, 'accounts/forgot_password.html')


def reset_password(request, uidb64, token):
    # Decode user from URL
    try:
        uid  = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (User.DoesNotExist, ValueError, TypeError):
        user = None

    # Validate token
    if user is None or not default_token_generator.check_token(user, token):
        return render(request, 'accounts/reset_password.html', {
            'invalid': True
        })

    if request.method == 'POST':
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')

        if len(password1) < 8:
            return render(request, 'accounts/reset_password.html', {
                'uidb64': uidb64,
                'token': token,
                'error': 'Password must be at least 8 characters.'
            })

        if password1 != password2:
            return render(request, 'accounts/reset_password.html', {
                'uidb64': uidb64,
                'token': token,
                'error': 'Passwords do not match.'
            })

        user.set_password(password1)
        user.save()
        return render(request, 'accounts/reset_password.html', {
            'success': True
        })

    return render(request, 'accounts/reset_password.html', {
        'uidb64': uidb64,
        'token': token,
    })