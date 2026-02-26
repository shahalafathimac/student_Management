from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from student.models import Student


class RegisterForm(UserCreationForm):

    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    gender = forms.ChoiceField(
        choices=[
            ('', 'Select Gender'),
            ('Male', 'Male'),
            ('Female', 'Female'),
        ],
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=True
    )

    age = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    reg_number = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    department = forms.ChoiceField(
        choices=Student.DEPARTMENT_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=True
    )

    year_of_admission = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    phone_number = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    profile_picture = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    agree = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        required=True
    )

    class Meta:
        model = CustomUser
        fields = [
            'first_name',
            'last_name',
            'email',
            'profile_picture',
            'password1',
            'password2'
        ]

    # ✅ Email Validation
    def clean_email(self):
        email = self.cleaned_data.get('email')

        if CustomUser.objects.filter(username=email).exists():
            raise forms.ValidationError("This email is already registered.")

        return email

    # ✅ Save Method
    def save(self, commit=True):
        user = super().save(commit=False)

        user.username = self.cleaned_data['email']
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.profile_picture = self.cleaned_data.get('profile_picture')
        user.gender = self.cleaned_data['gender']

        if commit:
            user.save()

            Student.objects.create(
                user=user,
                age=self.cleaned_data.get('age'),
                reg_number=self.cleaned_data['reg_number'],
                department=self.cleaned_data['department'],
                year_of_admission=self.cleaned_data['year_of_admission'],
                phone_number=self.cleaned_data.get('phone_number'),
            )

        return user