from django.db import models
from django.contrib.auth.models import AbstractUser
from user.models import Courses, User as Instructor
from datetime import datetime

class Exam(models.Model):
    name = models.CharField(max_length=200)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    start_time = models.DateTimeField(default=datetime.now())
    end_time = models.DateTimeField(default=datetime.now())
    max_marks = models.IntegerField(default = 0)
    def __str__(self):
        return self.name

class SubjectiveExam(models.Model):
    name = models.CharField(max_length=200)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    qno = models.IntegerField()
    def __str__(self):
        return self.name

class SubjectiveExamTaken(models.Model):
    exam = models.ForeignKey(SubjectiveExam, on_delete=models.CASCADE)
    q_index = models.IntegerField(default = 0)
    user = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    marks = models.IntegerField(default=0)
    remarks = models.TextField(null=True)
    corrected_by = models.ForeignKey(Instructor, on_delete=models.CASCADE, null=True, related_name='+')
    def __str__(self):
        return "Answer for question " + str(self.q_index)

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
    positive_marks = models.IntegerField(default = 3)
    negative_marks = models.IntegerField(default = -1)
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
    def __str__(self):
        return "QB: "+str(self.topic)+": "+str(self.question_text)

