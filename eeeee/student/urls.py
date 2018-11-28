from django.urls import include,path

from . import views

urlpatterns = [
	path('login/',views.login,name='login_student'),
	path('newstudent/',views.newstudent,name='newstudent'),
	path('', views.index),
	path('exam_paper/<int:exam_id>',views.take_exam,name='take_exam'),
	path('completed_paper/<int:exam_id>',views.completed_exam,name='completed_exam'),
	path('view_exam/<int:eid>/<int:uid>', views.questions),
    path('question/<int:eid>/<int:uid>/<int:index>', views.show_question),
]