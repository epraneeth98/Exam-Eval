from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Courses(models.Model):
    course_id = models.CharField(max_length=200)
    department = models.CharField(max_length=200)

    def __str__(self):
        return self.course_id

class Instructor(User):
    department = models.CharField(max_length=200)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)

    def __str__(self):
        return self.username

class Exam(models.Model):
    name = models.CharField(max_length=200)
    instructor = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateField()
    end_time = models.DateField()

    def __str__(self):
        return self.name

class Question(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=500)
    choice1 = models.CharField(max_length=200)
    choice2 = models.CharField(max_length=200)
    choice3 = models.CharField(max_length=200)
    answer = models.IntegerField()
