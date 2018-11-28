from django.http import HttpResponse, HttpResponseRedirect
from .forms import LoginForm#,NewInstructorForm
from django.shortcuts import render
from instructor.models import Instructor

def login_redirect(request):
    return render(request, 'login_redirect.html')
