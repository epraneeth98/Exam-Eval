from django.urls import include,path

from . import views

urlpatterns = [
	path('login/',views.login,name='login_student'),
	path('newstudent/',views.newstudent,name='newstudent'),
	path('', views.index),
]