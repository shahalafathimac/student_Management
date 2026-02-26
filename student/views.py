from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Student

@login_required
def student_dashboard(request):
    student = Student.objects.get(user=request.user)
    return render(request, 'student/dashboard.html', {'student': student})