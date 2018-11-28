from django import forms
from .models import Student, Answer # Exam, Question, 

class NewStudentForm(forms.ModelForm):
    class Meta :
        model = Student
        fields = ['username','password','first_name','last_name','email','department','course']

class AnswerForm(forms.ModelForm):
    class Meta :
        model = Answer
        fields = ['answer']