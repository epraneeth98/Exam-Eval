from django.http import HttpResponse, HttpResponseRedirect
from .forms import NewExamForm, NewQuestionForm, NewInstructorForm, NewTopicForm, NewQuestionInQBForm, NewSubExamForm
from user.forms import LoginForm
from django.shortcuts import render
from user.models import User as Instructor
from student.models import ExamTaken,Answer
from .models import Exam, Question, Topic, Question_Bank, SubjectiveExamTaken, SubjectiveExamTaken, SubjectiveExam
import operator


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        username = form.data['username']
        password = form.data['password']
        instructor = Instructor.objects.all().filter(username = username).filter(password = password)
        # user = Instructor.authenticate(request, username=username, password=password)
        if form.is_valid():
            if len(instructor)==0 :
                return render(request, 'instructor_login.html', {'form': form})
            else:
                request.session['username'] = username
                return HttpResponseRedirect('/instructor')
    else:
        form = LoginForm()
    return render(request, 'instructor_login.html', {'form': form})

def subm_results(request, exam_id):
    username = request.session['username']
    instructor = Instructor.objects.get(username = username)
    exam = Exam.objects.get(id=exam_id)
    instructor = exam.instructor
    instr_course= instructor.course
    student_set = Instructor.objects.all().filter(is_student=True, is_instructor=False, course=instr_course)
    examtaken_set = ExamTaken.objects.all().filter(exam__id=exam_id).order_by('marks_obtained')[:30]
    print(student_set)
    print(examtaken_set)
    return render(request, 'subm_results.html', {'examtaken_set':examtaken_set})    


def new_subjective_exam(request):
    instructor = request.session['username']
    if request.method == 'POST':
        form = NewSubExamForm(request.POST)
        if form.is_valid():
            exam = form.save(commit=False)
            exam.instructor = Instructor.objects.get(username = instructor)
            exam.save()
            r = exam.qno+1
            s = Instructor.objects.all().filter(is_student = True).filter(course = exam.instructor.course)
            for x in range(1, r):
                for student in s:
                    SubjectiveExamTaken.objects.create(user = student, q_index = x, exam = exam)
            return HttpResponseRedirect('/instructor')
        else:
            return render(request, 'new_exam.html', {'form': form})
            

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NewSubExamForm()

    return render(request, 'new_exam.html', {'form': form})


def newinstructor(request):
    if request.method == 'POST':
        form = NewInstructorForm(request.POST)
        username=form.data['username']
        if form.is_valid():
            newinstr=form.save(commit = False)
            newinstr.is_student = False
            newinstr.is_instructor = True
            newinstr.save()
            request.session['username'] = newinstr.username
            return HttpResponseRedirect('/instructor/login')
    else:
        form = NewInstructorForm()
    return render(request, 'newinstructor.html', {'form': form})

def index(request):
    username = request.session['username']
    instructor = Instructor.objects.get(username = username)
    exams_set = Exam.objects.filter(instructor = instructor)
    exams_set1 = SubjectiveExam.objects.filter(instructor__course = instructor.course)
    return render(request, 'instructor.html', {'instructor': instructor, 'exams_set':exams_set, 'exams_set2':exams_set1})

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
	return render(request, 'edit_exam.html', {'form': form, 'exam_id':exam_id})

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
            ee = Exam.objects.get(id = exam_id)
            exam.save()
            if "continue" in request.POST:
            	return HttpResponseRedirect('/instructor/new_question/'+str(exam_id))
            else :
                q_set = Question.objects.filter(exam__id = exam_id)
                x = 0
                for i in q_set:
                    x = x + i.positive_marks
                ee.max_marks=x
                ee.save()
                return HttpResponseRedirect('/instructor')
        else:
        	return render(request, 'new_question.html', {'form': form})
    else:
        form = NewQuestionForm()

    return render(request, 'new_question.html', {'form': form, 'exam_id':exam_id})

def show_exam(request, exam_id):
	exam = Exam.objects.get(id=exam_id)
	questions_set = Question.objects.filter(exam=exam)
	print(questions_set[0].question_text)
	return render(request, 'show_exam.html', {'questions_set':questions_set, 'exam':exam})

def topics_in_qb(request):
    username = request.session['username']
    instructor = Instructor.objects.get(username = username)
    course = instructor.course
    topics_set = Topic.objects.filter(course = instructor.course)
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.course = course
            topic.save()
            return HttpResponseRedirect('/instructor/topics_in_qb')
        else:
            return HttpResponseRedirect('/instructor/topics_in_qb')
    else:
        form = NewTopicForm()
        return render(request, 'topics_in_qb.html', {'form':form,'instructor': instructor, 'topics_set':topics_set})

def show_questions_in_topic(request, topic_id):
    username = request.session['username']
    instructor = Instructor.objects.get(username = username)
    topic = Topic.objects.get(id = topic_id)
    course = instructor.course
    department = course.department
    questions_set = Question_Bank.objects.filter(topic__id = topic_id)
    if request.method == 'POST':
        form = NewQuestionInQBForm(request.POST)
        if form.is_valid():
            new_q = form.save(commit=False)
            new_q.course = course
            new_q.topic = topic
            new_q.department=department
            new_q.save()
            return HttpResponseRedirect('/instructor/look_questions/'+str(topic_id))
        else:
            return HttpResponseRedirect('/instructor/look_questions/'+str(topic_id))
    else:
        form = NewQuestionInQBForm()
        return render(request, 'show_questions_in_topic.html', {'form':form,'topic':topic, 'questions_set':questions_set})

def logout(request):
    try:
        username = request.session['username']
        request.session.flush()

    except KeyError:
        pass
    return HttpResponseRedirect('/')

def new_question_from_db(request, exam_id, question_bank_qid):
    instructor = request.session['username']
    e = Exam.objects.get(id = exam_id)
    if request.method == 'POST':
        form = NewQuestionForm(request.POST)
        if form.is_valid():
            exam1 = form.save(commit=False)
            exam1.exam = Exam.objects.get(id = exam_id)
            ee = Exam.objects.get(id = exam_id)
            #exam1.save()
            if "continue" in request.POST:
                return HttpResponseRedirect('/instructor/new_question/'+str(exam_id))
            else :
                q_set = Question.objects.filter(exam__id = exam_id)
                x = 0
                for i in q_set:
                    x = x + i.positive_marks
                ee.max_marks=x
                ee.save()
                return HttpResponseRedirect('/instructor')
        else:
            return render(request, 'new_question.html', {'form': form})
            

    # if a GET (or any other method) we'll create a blank form
    else:
        q = Question_Bank.objects.get(id = question_bank_qid)
        question = Question.objects.create(exam=e,question_text=q.question_text,choice1=q.choice1,choice2=q.choice2,choice3=q.choice3,answer=q.answer)
        form = NewQuestionForm(instance=question)

    return render(request, 'new_question.html', {'form': form})

def qb(request, exam_id):
    username = request.session['username']
    instructor = Instructor.objects.get(username = username)
    q = Question_Bank.objects.all()
    return render(request, 'questionbank.html', {'qb': q, 'exam_id': exam_id})

def ts(request, exam_id):
    username = request.session['username']
    instructor = Instructor.objects.get(username = username)
    course = instructor.course
    topics_set = Topic.objects.filter(course = instructor.course)
    return render(request, 'topic_select.html', { 'topics_set':topics_set, 'exam_id': exam_id})
