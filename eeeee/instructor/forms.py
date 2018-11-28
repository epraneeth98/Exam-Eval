from django import forms
from .models import Exam, Question, Instructor, Topic, Question_Bank, SubjectiveExam, SubjectiveExamTaken

class NewExamForm(forms.ModelForm):
    class Meta :
    	model = Exam
    	fields = ['name','start_time','end_time']	

class NewQuestionForm(forms.ModelForm):
	class Meta :
		model = Question
		fields = ['question_text','choice1','choice2','choice3','answer','positive_marks','negative_marks']


class NewInstructorForm(forms.ModelForm):
    class Meta :
        model = Instructor
        fields = ['username','password','first_name','last_name','email','department','course']

class NewTopicForm(forms.ModelForm):
    class Meta :
        model = Topic
        fields = ['topic_name']
        labels = {
            'topic_name':'Add New Topic',
        }

class NewQuestionInQBForm(forms.ModelForm):
    class Meta :
        model = Question_Bank
        fields = ['question_text','choice1','choice2','choice3','answer']

class NewSubExamForm(forms.ModelForm):
    class Meta :
        model = SubjectiveExam
        fields = ['name','qno']

class SubjectiveExamTakenForm(forms.ModelForm):
    class Meta :
        model = SubjectiveExamTaken
        fields = ['marks','remarks']