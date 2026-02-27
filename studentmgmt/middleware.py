from django.shortcuts import redirect
from django.urls import reverse


class RoleBasedAccessMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # Allow admin URLs always
        if request.path.startswith('/admin/'):
            return self.get_response(request)

        # Allow login, register, home
        public_urls = [
            reverse('login'),
            reverse('register'),
            reverse('home'),
        ]

        if request.path in public_urls:
            return self.get_response(request)

        # If not logged in
        if not request.user.is_authenticated:
            return redirect('login')

        # Role restriction
        if request.user.role == 'principal':
            if request.path.startswith('/student/'):
                return redirect('principal_dashboard')

        if request.user.role == 'student':
            if request.path.startswith('/principal/'):
                return redirect('student_dashboard')

        return self.get_response(request)