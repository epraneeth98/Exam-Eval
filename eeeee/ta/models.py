from django.db import models
from user.models import User
from instructor.models import Question
# Create your models here.

class Message(models.Model):
    text = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    time = models.DateTimeField(auto_now=True)

class QuestionCorrection(models.Model):
    question = models.ForeignKey(Question, on_delete = models.CASCADE)
    ta = models.ForeignKey(User, on_delete = models.CASCADE)
    student = models.ForeignKey(User, on_delete = models.CASCADE, related_name='+')
    marks = models.IntegerField()
    no_crib = models.BooleanField(default=True)