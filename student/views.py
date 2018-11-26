from django.http import HttpResponse, HttpResponseRedirect
from .forms import NewStudentForm # NewExamForm, NewQuestionForm, 
from user.forms import LoginForm
from django.shortcuts import render
from user.models import User as Student
#from .models import Exam, Question, Topic

def login(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = LoginForm(request.POST)
        username = form.data['username']
        password = form.data['password']
        student = Student.objects.all().filter(username = username).filter(password = password)
        if form.is_valid():
            if len(student)==0 :
                return render(request, 'student_login.html', {'form': form})
            else:
                request.session['username'] = username
                return HttpResponseRedirect('/student')
    else:
        form = LoginForm()
    return render(request, 'student_login.html', {'form': form})

def newstudent(request):
    if request.method == 'POST':
        form = NewStudentForm(request.POST)
        username=form.data['username']
        if form.is_valid():
            newstud=form.save(commit = False)
            newstud.is_student = True
            newstud.is_instructor = False
            newstud.save()
            request.session['username'] = newstud.username
            return HttpResponse(newstud.username)
    else:
        form = NewStudentForm()
    return render(request, 'newstudent.html', {'form': form})

def index(request):
	username = request.session['username']
	student = Student.objects.get(username = username)
	return render(request, 'student.html', {'student': student})