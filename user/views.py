from django.http import HttpResponse, HttpResponseRedirect
from .forms import LoginForm#,NewInstructorForm
from django.shortcuts import render
from instructor.models import Instructor

def login_redirect(request):
    return render(request, 'login_redirect.html')


# def newinstructor(request):
#     if request.method == 'POST':
#         form = NewInstructorForm(request.POST)
#         department=form.data['department']
#         course=form.data['course']
#         first_name=form.data['first_name']
#         last_name=form.data['last_name']
#         email=form.data['email']
#         username=form.data['username']
#         password=form.data['password']
#         if form.is_valid():
#             newinstr=form.save(commit = False)
#             newinstr.save()
#             request.session['username'] = username
#             return HttpResponse('instructor')
#     else:
#         form = NewInstructorForm()
#     return render(request, 'newinstructor.html', {'form': form})

