from django.db import models
from django.contrib.auth.models import AbstractUser
from user.models import Courses, User as Instructor

# Create your models here.

class Exam(models.Model):
    name = models.CharField(max_length=200)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    start_time = models.DateField()
    end_time = models.DateField()
    def __str__(self):
        return self.name

class Topic(models.Model):
    course=models.ForeignKey(Courses,on_delete=models.CASCADE)
    topic_name=models.CharField(max_length=200)
    def __str__(self):
        return self.topic_name

class Question(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=500)
    choice1 = models.CharField(max_length=200)
    choice2 = models.CharField(max_length=200)
    choice3 = models.CharField(max_length=200)
    answer = models.IntegerField()

class Question_Bank(models.Model):
    department = models.CharField(max_length=200)
    course=models.ForeignKey(Courses,on_delete=models.CASCADE)
    topic=models.ForeignKey(Topic, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=500)
    choice1 = models.CharField(max_length=200)
    choice2 = models.CharField(max_length=200)
    choice3 = models.CharField(max_length=200)
    answer = models.IntegerField()

