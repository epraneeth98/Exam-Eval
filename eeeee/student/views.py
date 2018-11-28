from django.http import HttpResponse, HttpResponseRedirect
from .forms import NewStudentForm, AnswerForm # NewExamForm, NewQuestionForm, 
from user.forms import LoginForm
from django.shortcuts import render
from user.models import User as Student
from instructor.models import Exam, Question, SubjectiveExam, SubjectiveExamTaken
from .models import ExamTaken, Answer
from datetime import datetime

def login(request):
    if request.method == 'POST':
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
            # request.session['username'] = newstud.username
            return HttpResponseRedirect('/student/login')
    else:
        form = NewStudentForm()
    return render(request, 'newstudent.html', {'form': form})

def newta(request):
    if request.method == 'POST':
        form = NewStudentForm(request.POST)
        username=form.data['username']
        if form.is_valid():
            newstud=form.save(commit = False)
            newstud.is_student = False
            newstud.is_instructor = False
            newstud.save()
            #request.session['username'] = newstud.username
            return HttpResponseRedirect('/ta/login')
    else:
        form = NewStudentForm()
    return render(request, 'newstudent.html', {'form': form})

def index(request):
	username = request.session['username']
	now=datetime.now()
	print(now)
	student = Student.objects.get(username = username)
	student_course=student.course
	exam_set = Exam.objects.all().filter(instructor__course = student_course).filter(start_time__lte= now).filter(end_time__gte=now)
	exams_set =  SubjectiveExam.objects.all().filter(instructor__course = student.course)
	empty = Exam.objects.all().filter(id= -3)
	taken_examset = ExamTaken.objects.all().filter(user = student)
	print(taken_examset)
	for x in taken_examset:
		y=x.exam
		z=Exam.objects.all().filter(id = y.id)
		empty = empty | z
	to_take_examsset = exam_set.difference(empty)
	return render(request, 'student.html', {'exams_set':exams_set,'student': student,'taken_examset': taken_examset, 'to_take_examsset':to_take_examsset})

def completed_exam(request,exam_id):
	username = request.session['username']
	student = Student.objects.get(username = username)
	exam = Exam.objects.get(id = exam_id)
	exam_taken_details = ExamTaken.objects.get(user = student, exam =exam)
	print(exam_taken_details)
	answer_set = Answer.objects.all().filter(exam_taken=exam_taken_details)
	marks_obtained=0
	tot_marks=0
	for i in answer_set:
		if i.answer==i.question.answer:
			marks_obtained=marks_obtained+i.question.positive_marks
			tot_marks=tot_marks+i.question.positive_marks
		elif i.answer==0:
			tot_marks=tot_marks+i.question.positive_marks
		else:
			tot_marks=tot_marks+i.question.positive_marks
			marks_obtained=marks_obtained+i.question.negative_marks
	return render(request, 'completed_exam.html', {'answer_set': answer_set,'marks_obtained':marks_obtained,'tot_marks':tot_marks})

def take_exam(request, exam_id):
	username = request.session['username']
	student = Student.objects.get(username = username)
	exam = Exam.objects.get(id = exam_id)
	max_marks=exam.max_marks
	question_set = Question.objects.all().filter(exam = exam)
	forms = []
	if request.method == 'POST':
		i = 0
		x = 0
		just_taken_exam = ExamTaken.objects.create(exam=exam, user=student)
		for question in question_set:
			f = AnswerForm(request.POST, prefix="form"+str(i))
			answer = f.save(commit=False)
			answer.question = question
			answer.exam_taken = just_taken_exam
			answer.save()
			if answer.answer == 0:
				x=x+0
			elif answer.answer == answer.question.answer:
				x=x+answer.question.positive_marks
			else:
				x=x+answer.question.negative_marks
			i = i+1
		just_taken_exam.marks_obtained=x
		just_taken_exam.max_marks=max_marks
		just_taken_exam.save()

		return HttpResponseRedirect('/student')
	else:
		i = 0
		for question in question_set:
			f = AnswerForm(prefix="form"+str(i))
			forms.append(f)
			i = i+1
		q_f = zip(question_set, forms)
	return render(request, 'exam_paper.html', {'qf': q_f})


def questions(request, eid, uid):
    q = SubjectiveExamTaken.objects.all().filter(exam__id = eid, user__id = uid).order_by('q_index')
    return render(request, 'student_questions.html', {'q':q})

def show_question(request,eid,uid,index):
    x = "http://10.196.31.155:8080/media/documents/"
    username = Student.objects.all().filter(id = uid)[0].username
    examname = SubjectiveExam.objects.all().filter(id = eid)[0].name
    q = x+username+"_"+examname+"_"+str(index)
    mrm = SubjectiveExamTaken.objects.all().get(exam__id = eid, user__id = uid, q_index = index)
    return render(request, 'student_question.html', {'q':q, 'mrm': mrm, 'cb' : mrm.corrected_by})