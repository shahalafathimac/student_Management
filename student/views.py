from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q,Sum
from .models import Student,CoursePurchase
from accounts.decorators import role_required
from .forms import StudentProfileForm, UserUpdateForm
from django.contrib import messages
from principal.models import Course

@role_required(['student'])
def student_dashboard(request):
    student = get_object_or_404(Student, user=request.user)

    purchases = CoursePurchase.objects.filter(
        student=student
    ).select_related('course')

    approved = purchases.filter(status='Approved')
    pending  = purchases.filter(status='Pending')
    rejected = purchases.filter(status='Rejected')

    status_filter = request.GET.get('status')

    if status_filter == 'approved':
        filtered_courses = purchases.filter(status='Approved')
    elif status_filter == 'all':
        filtered_courses = purchases
    else:
        filtered_courses = approved

    total_spent = approved.aggregate(
        total=Sum('course__price')
    )['total'] or 0

    context = {
        'approved_count': approved.count(),
        'pending_count': pending.count(),
        'rejected_count': rejected.count(),
        'total_spent': total_spent,
        'approved_courses': filtered_courses,
        'all_courses': purchases,
        'filtered_courses': filtered_courses,
    }

    return render(request, 'student/dashboard.html', context)


@role_required(['student'])
def student_profile(request):
    student = get_object_or_404(
        Student.objects.select_related('user'),
        user=request.user
    )

    return render(request, 'student/profile.html', {
        'student': student
    })


@role_required(['student'])
def purchase_courses(request):
    student = get_object_or_404(Student, user=request.user)
    courses = Course.objects.all().order_by('department', 'title')

    purchase_map = {
        p.course_id: p.status
        for p in CoursePurchase.objects.filter(student=student).only('course_id', 'status')
    }
    for course in courses:
        course.purchase_status = purchase_map.get(course.id)

    # Fetch distinct departments directly from DB 
    departments = Course.objects.values_list('department', flat=True).distinct().order_by('department')

    if request.method == 'POST':
        selected_ids = request.POST.getlist('selected_courses')

        if not selected_ids:
            messages.warning(request, 'Please select at least one course.')
            return redirect('purchase_courses')

        enrolled = 0
        for course_id in selected_ids:
            course_obj = Course.objects.filter(id=course_id).first()
            if not course_obj:
                continue

            purchase, created = CoursePurchase.objects.get_or_create(
                student=student,
                course=course_obj,
                defaults={'status': 'Pending'}
            )

            if not created and purchase.status == 'Rejected':
                purchase.status = 'Pending'
                purchase.save(update_fields=['status'])
                enrolled += 1
            elif created:
                enrolled += 1

        if enrolled:
            messages.success(request, f'{enrolled} course request(s) submitted successfully!')
        else:
            messages.info(request, 'No new courses were submitted (already pending or approved).')

        return redirect('purchase_courses')

    return render(request, 'student/purchase_courses.html', {
        'courses':     courses,
        'departments': departments,  
    })


@login_required
def edit_profile(request):
    student = get_object_or_404(Student, user=request.user)

    if request.method == 'POST':
        user_form    = UserUpdateForm(request.POST, instance=request.user)
        student_form = StudentProfileForm(
            request.POST,
            request.FILES,      # profile_picture uploads work
            instance=student
        )

        if user_form.is_valid() and student_form.is_valid():
            user_form.save()
            student_form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('student_profile')  
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        user_form    = UserUpdateForm(instance=request.user)
        student_form = StudentProfileForm(instance=student)

    return render(request, 'student/edit_profile.html', {
        'user_form':    user_form,
        'student_form': student_form,
    })