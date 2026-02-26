from django.db import models
from django.conf import settings

class Student(models.Model):
    DEPARTMENT_CHOICES = [
        ('Computer Science', 'Computer Science'),
        ('Electronics and Communication', 'Electronics and Communication'),
        ('Mechanical Engineering', 'Mechanical Engineering'),
        ('Civil Engineering', 'Civil Engineering'),
        ('Business Administration', 'Business Administration'),
    ]

    user             = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    reg_number       = models.CharField(max_length=50)
    department       = models.CharField(max_length=100, choices=DEPARTMENT_CHOICES)
    year_of_admission = models.IntegerField()
    age              = models.IntegerField(null=True, blank=True)
    phone_number     = models.CharField(max_length=15, null=True, blank=True)
    profile_picture  = models.ImageField(              # ← ADD THIS
        upload_to='student_avatars/',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.user.username
    

class CoursePurchase(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    )

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey("principal.Course", on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.user.username} - {self.course.title}"