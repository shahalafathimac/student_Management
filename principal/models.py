from django.db import models

# Create your models here.

class Course(models.Model):

    DEPARTMENT_CHOICES = [
        ('Computer Science', 'Computer Science'),
        ('Electronics and Communication', 'Electronics and Communication'),
        ('Mechanical Engineering', 'Mechanical Engineering'),
        ('Civil Engineering', 'Civil Engineering'),
        ('Business Administration', 'Business Administration'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()

    department = models.CharField(
        max_length=100,
        choices=DEPARTMENT_CHOICES
    )

    price = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    