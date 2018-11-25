from django.db import models
from django.contrib.auth.models import AbstractUser

class Courses(models.Model):
    course_id = models.CharField(max_length=200)
    department = models.CharField(max_length=200)
    def __str__(self):
        return self.course_id

class User(AbstractUser):
    is_student = models.BooleanField(default=True)
    is_instructor = models.BooleanField(default=False)
    department = models.CharField(max_length=200)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.username

