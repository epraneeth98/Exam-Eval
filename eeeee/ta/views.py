from django.shortcuts import render, HttpResponseRedirect
from user.forms import LoginForm
from user.models import User as TA
from instructor.models import Exam, Question, SubjectiveExam, SubjectiveExamTaken
from student.models import ExamTaken
from instructor.forms import SubjectiveExamTakenForm

# Create your views here.

def login(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        print('here1')
        # create a form instance and populate it with data from the request:
        form = LoginForm(request.POST)
        username = form.data['username']
        password = form.data['password']
        instructor = TA.objects.all().filter(username = username).filter(password = password)
        # user = Instructor.authenticate(request, username=username, password=password)
        if form.is_valid():
            if len(instructor)==0 :
                print('here2')
                return render(request, 'ta_login.html', {'form': form})
            else:
                request.session['username'] = username
                return HttpResponseRedirect('/ta')
    else:
        form = LoginForm()
    return render(request, 'ta_login.html', {'form': form})


def index(request):
	username = request.session['username']
	ta = TA.objects.get(username = username)
	exams_set =  SubjectiveExam.objects.all().filter(instructor__course = ta.course)
	return render(request, 'ta.html', {'ta': ta, 'exams_set':exams_set})

def exam_students(request, exam_id):
    username = request.session['username']
    ta = TA.objects.get(username = username)
    es = SubjectiveExam.objects.get(id = exam_id)
    es = TA.objects.all().filter(is_student = True).filter(course = es.instructor.course)
    return render(request, 'exam_students.html', {'es':es, 'exam_id':exam_id})

def questions(request, eid, uid):
    q = SubjectiveExamTaken.objects.all().filter(exam__id = eid, user__id = uid).order_by('q_index')
    return render(request, 'questions.html', {'q':q})

def show_question(request,eid,uid,index):
    x = "http://10.196.31.155:8080/media/documents/"
    username = TA.objects.all().filter(id = uid)[0].username
    examname = SubjectiveExam.objects.all().filter(id = eid)[0].name
    q = x+username+"_"+examname+"_"+str(index)
    mrm = SubjectiveExamTaken.objects.all().get(exam__id = eid, user__id = uid, q_index = index)
    if request.method == 'POST':
        form = SubjectiveExamTakenForm(request.POST, instance=mrm)
        if form.is_valid():
            exam = form.save(commit=False)
            exam.corrected_by = TA.objects.get(username = request.session['username'])
            exam.save()
            return HttpResponseRedirect('/ta/correct_exam/'+str(eid)+'/'+str(uid))
        else:
            return render(request, 'question.html', {'q':q, 'form': form})
    else:
        form = SubjectiveExamTakenForm(instance=mrm)
    return render(request, 'question.html', {'q':q, 'form':form, 'cb' : mrm.corrected_by})
