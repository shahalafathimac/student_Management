from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .models import Student,CoursePurchase
from accounts.decorators import role_required
from .forms import StudentProfileForm, UserUpdateForm
from django.contrib import messages

@role_required(['student'])
def student_dashboard(request):
    student = get_object_or_404(Student, user=request.user)

    purchases = CoursePurchase.objects.filter(student=student).select_related('course')

    approved_purchases = purchases.filter(status='Approved')
    pending_purchases  = purchases.filter(status='Pending')
    rejected_purchases = purchases.filter(status='Rejected')

    # Sum the price of all approved courses
    total_spent = approved_purchases.aggregate(
        total=Sum('course__price')
    )['total'] or 0

    # Build a list of approved course objects with the fields the template uses:
    # course.name  → maps to course.title
    # course.department
    approved_courses = [
        {
            'name': p.course.title,
            'department': p.course.department,
        }
        for p in approved_purchases
    ]

    context = {
        'approved_count':  approved_purchases.count(),
        'pending_count':   pending_purchases.count(),
        'rejected_count':  rejected_purchases.count(),
        'total_spent':     total_spent,
        'approved_courses': approved_courses,
    }

    return render(request, 'student/dashboard.html', context)


@role_required(['student'])
def student_profile(request):
    return render(request, 'student/profile.html')


@role_required(['student'])
def purchase_courses(request):
    return render(request, 'student/purchase_courses.html')


@login_required
def edit_profile(request):
    student = get_object_or_404(Student, user=request.user)

    if request.method == 'POST':
        user_form    = UserUpdateForm(request.POST, instance=request.user)
        student_form = StudentProfileForm(
            request.POST,
            request.FILES,      # ← required so profile_picture uploads work
            instance=student
        )

        if user_form.is_valid() and student_form.is_valid():
            user_form.save()
            student_form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('student_profile')   # send back to profile page
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        user_form    = UserUpdateForm(instance=request.user)
        student_form = StudentProfileForm(instance=student)

    return render(request, 'student/edit_profile.html', {
        'user_form':    user_form,
        'student_form': student_form,
    })