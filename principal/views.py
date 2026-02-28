from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from student.models import Student
from . import models
from .models import Course
from django.db.models import Q
from .forms import CourseForm, StudentEditForm
from accounts.decorators import role_required
from student.models import CoursePurchase

@role_required(['principal'])
def principal_dashboard(request):
    from student.models import CoursePurchase

    total_students    = Student.objects.count()
    total_courses     = Course.objects.count()
    total_departments = Course.objects.values('department').distinct().count()
    pending_requests  = CoursePurchase.objects.filter(status='Pending').count()

    quick_approvals = CoursePurchase.objects.select_related(
        'student__user', 'course'
    ).filter(status='Pending').order_by('-created_at')[:5]

    recent_students = Student.objects.select_related('user').order_by(
        '-user__date_joined'
    )[:5]

    return render(request, 'principal/dashboard.html', {
        'total_students':    total_students,
        'total_courses':     total_courses,
        'total_departments': total_departments,
        'pending_requests':  pending_requests,
        'quick_approvals':   quick_approvals,
        'recent_students':   recent_students,
    })

@role_required(['principal'])
def manage_courses(request):
    courses = Course.objects.all().order_by('-created_at')
    form = CourseForm()

    # Departments from DB — auto-updates when new depts are added
    departments = Course.objects.values_list(
        'department', flat=True
    ).distinct().order_by('department')

    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course added successfully.')
            return redirect('manage_courses')
        else:
            messages.error(request, 'Please fix the errors below.')

    return render(request, 'principal/manage_courses.html', {
        'courses':     courses,
        'form':        form,
        'departments': departments,  
    })

@role_required(['principal'])
def edit_course(request, pk):
    
    course = get_object_or_404(Course, pk=pk)
    form = CourseForm(instance=course)           # pre-populate on GET

    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)   # bind POST data to existing instance
        if form.is_valid():
            form.save()
            messages.success(request, f'"{course.title}" updated successfully.')
            return redirect('manage_courses')
        else:
            messages.error(request, 'Please fix the errors below.')

    return render(request, 'principal/edit_course.html', {
        'form': form,
        'course': course,
    })

@role_required(['principal'])
def delete_course(request, pk):
    
    course = get_object_or_404(Course, pk=pk)

    if request.method == 'POST':
        course_title = course.title
        course.delete()
        messages.success(request, f'"{course_title}" deleted successfully.')
        return redirect('manage_courses')

    return redirect('manage_courses')   # safe fallback for GET

@role_required(['principal'])
def manage_students(request):
    students = Student.objects.select_related('user').all()

    # Optional search by name or email
    query = request.GET.get('q', '').strip()
    if query:
        students = students.filter(
            models.Q(user__first_name__icontains=query) |
            models.Q(user__last_name__icontains=query)  |
            models.Q(user__email__icontains=query)
        )

    # Optional filter by department
    dept_filter = request.GET.get('department', '').strip()
    if dept_filter:
        students = students.filter(department=dept_filter)

     
    departments = Course.DEPARTMENT_CHOICES

    return render(request, 'principal/manage_students.html', {
        'students': students,
        'query': query,
        'dept_filter': dept_filter,
        'departments': departments,
    })

@role_required(['principal'])
def view_student(request, pk):
    student = get_object_or_404(Student.objects.select_related('user'), pk=pk)
    return render(request, 'principal/view_student.html', {'student': student})

@role_required(['principal'])
def course_approvals(request):

    if request.method == "POST":
        request_id = request.POST.get("request_id")
        action = request.POST.get("action")

        purchase = get_object_or_404(CoursePurchase, id=request_id)

        if action == "approve":
            purchase.status = "Approved"
            messages.success(request, "Course approved successfully.")
        elif action == "reject":
            purchase.status = "Rejected"
            messages.success(request, "Course rejected successfully.")

        purchase.save()
        return redirect("course_approvals")

    pending_requests = CoursePurchase.objects.select_related(
        'student__user', 'course'
    ).all().order_by('-created_at')

    return render(request, 'principal/course_approvals.html', {
        'pending_requests': pending_requests
    })

@role_required(['principal'])
def edit_student(request, pk):
    student = get_object_or_404(Student.objects.select_related('user'), pk=pk)

    if request.method == 'POST':
        form = StudentEditForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, f'Student "{student.user.first_name}" updated successfully.')
            return redirect('manage_students')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = StudentEditForm(instance=student)

    return render(request, 'principal/edit_student.html', {
        'form': form,
        'student': student,
    })