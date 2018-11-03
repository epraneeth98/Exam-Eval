from django.http import HttpResponse, HttpResponseRedirect
from .forms import LoginForm,NewInstructorForm
from django.shortcuts import render
from instructor.models import User as Instructor

def login(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = LoginForm(request.POST)
        username = form.data['username']
        password = form.data['password']
        instructor = Instructor.objects.all().filter(username = username).filter(password = password)
        # user = Instructor.authenticate(request, username=username, password=password)
        if form.is_valid():
            if len(instructor)==0 :
                return render(request, 'name.html', {'form': form})
            else:
                request.session['username'] = username
                # return HttpResponse(instructor[0])
                return HttpResponseRedirect('/instructor')

    else:
        form = LoginForm()

    return render(request, 'name.html', {'form': form})


def newinstructor(request):
    if request.method == 'POST':
        form = NewInstructorForm(request.POST)
        # department=form.data['department']
        # course=form.data['course']
        # first_name=form.data['first_name']
        # last_name=form.data['last_name']
        # email=form.data['email']
        username=form.data['username']
        # password=form.data['password']
        if form.is_valid():
            newinstr=form.save(commit = False)
            newinstr.save()
            request.session['username'] = username
            return HttpResponse('instructor')
    else:
        form = NewInstructorForm()
    return render(request, 'newinstructor.html', {'form': form})

