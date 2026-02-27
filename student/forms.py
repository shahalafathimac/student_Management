from django import forms
from .models import Student
from django.contrib.auth import get_user_model

User = get_user_model()


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'reg_number',
            'department',
            'year_of_admission',
            'age',
            'phone_number',
            'profile_picture', 
        ]


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']