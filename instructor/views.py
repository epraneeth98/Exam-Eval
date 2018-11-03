from django.http import HttpResponse, HttpResponseRedirect
from .forms import NewExamForm, NewQuestionForm
from django.shortcuts import render
from instructor.models import User as Instructor, Exam, Question


def index(request):
	username = request.session['username']
	instructor = Instructor.objects.get(username = username)
	exams_set = Exam.objects.filter(instructor = instructor)
	return render(request, 'instructor.html', {'instructor': instructor, 'exams_set':exams_set})

def new_exam(request):
    instructor = request.session['username']

    if request.method == 'POST':
        form = NewExamForm(request.POST)
        
        if form.is_valid():
            exam = form.save(commit=False)
            exam.instructor = Instructor.objects.get(username = instructor)
            exam.save()
            id = exam.id
            return HttpResponseRedirect('/instructor/new_question/'+str(id))
        else:
        	return render(request, 'new_exam.html', {'form': form})
            

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NewExamForm()

    return render(request, 'new_exam.html', {'form': form})

def edit_exam(request, exam_id):
	exam = Exam.objects.get(pk = exam_id)
	if request.method == 'POST':
		form = NewExamForm(request.POST, instance=exam)
		if form.is_valid():
			exam = form.save(commit=False)
			exam.save()
			id = exam.id
			return HttpResponseRedirect('/instructor/exam/'+str(id))
		else:
			return render(request, 'edit_exam.html', {'form': form})
	else:
		form = NewExamForm(instance=exam)
	return render(request, 'edit_exam.html', {'form': form})

def edit_question(request, question_id):
	q = Question.objects.get(pk = question_id)
	if request.method == 'POST':
		form = NewQuestionForm(request.POST, instance=q)
		if form.is_valid():
			question = form.save(commit=False)
			question.save()
			return HttpResponseRedirect('/instructor/exam/'+str(q.exam.id))
		else:
			return render(request, 'edit_question.html', {'form': form})
	else:
		form = NewQuestionForm(instance=q)
	return render(request, 'edit_question.html', {'form': form})



def new_question(request, exam_id):
    instructor = request.session['username']

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NewQuestionForm(request.POST)
        
        if form.is_valid():
            exam = form.save(commit=False)
            exam.exam = Exam.objects.get(id = exam_id)
            exam.save()
            if "continue" in request.POST:
            	return HttpResponseRedirect('/instructor/new_question/'+str(exam_id))
            else :
            	return HttpResponseRedirect('/instructor')
        else:
        	return render(request, 'new_question.html', {'form': form})
            

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NewQuestionForm()

    return render(request, 'new_question.html', {'form': form})

def show_exam(request, exam_id):
	exam = Exam.objects.get(id=exam_id)
	questions_set = Question.objects.filter(exam=exam)
	print(questions_set[0].question_text)
	return render(request, 'show_exam.html', {'questions_set':questions_set, 'exam':exam})

def logout(request):
    try:
        username = request.session['username']
        del request.session['username']
    except KeyError:
        pass
    return HttpResponseRedirect('/')








