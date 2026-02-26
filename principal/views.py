from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from student.models import Student
from .models import Course
from .forms import CourseForm, StudentEditForm
from accounts.decorators import role_required

@role_required(['principal'])
def principal_dashboard(request):
    students = Student.objects.all()
    return render(request, 'principal/dashboard.html', {'students': students})

@role_required(['principal'])
def manage_courses(request):
    """
    GET  → show all courses + blank Add form
    POST → validate & save new course, then redirect (PRG pattern)
    """
    courses = Course.objects.all().order_by('-created_at')
    form = CourseForm()

    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course added successfully.')
            return redirect('manage_courses')          # PRG – avoids duplicate submit on refresh
        else:
            messages.error(request, 'Please fix the errors below.')

    return render(request, 'principal/manage_courses.html', {
        'courses': courses,
        'form': form,
    })

@role_required(['principal'])
def edit_course(request, pk):
    """
    GET  → pre-fill form with existing course data
    POST → validate & save changes, then redirect
    """
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
    """
    POST only → delete course and redirect.
    GET requests are silently redirected back (no accidental deletes from URL bar).
    """
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

    from principal.models import Course  # reuse DEPARTMENT_CHOICES
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
    return render(request, 'principal/course_approvals.html')

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