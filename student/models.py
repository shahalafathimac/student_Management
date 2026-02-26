from django.db import models
from django.conf import settings

# Create your models here.


class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    reg_number = models.CharField(max_length=50)
    department = models.CharField(max_length=100)
    year_of_admission = models.IntegerField()

    age = models.IntegerField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return self.user.username