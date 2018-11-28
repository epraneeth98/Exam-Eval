from django.db import models
from django.contrib.auth.models import AbstractUser
from user.models import Courses, User as Student
from instructor.models import Exam, Question

class ExamTaken(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    user = models.ForeignKey(Student, on_delete=models.CASCADE)
    marks_obtained = models.IntegerField(default=-1000)
    max_marks = models.IntegerField(default=-1000)
    def __str__(self):
        return str(self.exam)

class Answer(models.Model):
	question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='+')
	exam_taken = models.ForeignKey(ExamTaken, on_delete=models.CASCADE)
	answer = models.IntegerField(default = 0)