from django import forms
from .models import Course
from student.models import Student
from django.contrib.auth import get_user_model



User = get_user_model()

DEPARTMENT_CHOICES = [
    ('Computer Science', 'Computer Science'),
    ('Electronics and Communication', 'Electronics and Communication'),
    ('Mechanical Engineering', 'Mechanical Engineering'),
    ('Civil Engineering', 'Civil Engineering'),
    ('Business Administration', 'Business Administration'),
]

class StudentEditForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100)
    last_name  = forms.CharField(max_length=100)
    

    class Meta:
        model  = Student
        fields = ['department']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial  = self.instance.user.last_name
            

    def save(self, commit=True):
        student = super().save(commit=False)
        student.user.first_name = self.cleaned_data['first_name']
        student.user.last_name  = self.cleaned_data['last_name']
        
        if commit:
            student.user.save()
            student.save()
        return student

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'department', 'price']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'e.g. Data Structures & Algorithms',
            }),
            'description': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Short course description...',
            }),
            'department': forms.Select(),
            'price': forms.NumberInput(attrs={
                'placeholder': '0.00',
                'min': '0',
                'step': '0.01',
            }),
        }