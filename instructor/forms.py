from django import forms
from .models import Exam, Question

class NewExamForm(forms.ModelForm):
    class Meta :
    	model = Exam
    	fields = ['name','start_time','end_time']	
    	widgets = {
            'start_time': forms.SelectDateWidget(),
            'end_time': forms.SelectDateWidget()
        }

class NewQuestionForm(forms.ModelForm):
	class Meta :
		model = Question
		fields = ['question_text','choice1','choice2','choice3','answer']
		