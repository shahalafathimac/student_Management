from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from student.models import Student

@login_required
def principal_dashboard(request):
    students = Student.objects.all()
    return render(request, 'principal/dashboard.html', {'students': students})