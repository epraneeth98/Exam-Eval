from django import forms
from instructor.models import Instructor

class LoginForm(forms.Form):
    username = forms.CharField(label='username', max_length=200)
    password = forms.CharField(label='password', max_length=200,widget=forms.PasswordInput)

class NewInstructorForm(forms.ModelForm):
    class Meta :
    	model = Instructor
    	fields = ['username','password','first_name','last_name','email','department','course']
