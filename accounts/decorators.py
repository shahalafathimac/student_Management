from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from functools import wraps


def role_required(allowed_roles=[]):
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapper(request, *args, **kwargs):

            if request.user.role in allowed_roles:
                return view_func(request, *args, **kwargs)

            # Redirect based on role
            if request.user.role == 'student':
                return redirect('student_dashboard')

            if request.user.role == 'principal':
                return redirect('principal_dashboard')

            return redirect('login')

        return wrapper
    return decorator