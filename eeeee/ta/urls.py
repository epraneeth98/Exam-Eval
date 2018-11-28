from django.urls import include,path

from . import views
from student import views as std_views

urlpatterns = [
	path('login/',views.login,name='login_ta'),
    path('', views.index),
    path('newta/',std_views.newta),
    path('exam/<int:exam_id>', views.exam_students),
    path('correct_exam/<int:eid>/<int:uid>', views.questions),
    path('question/<int:eid>/<int:uid>/<int:index>', views.show_question),
]
