"""ee URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import include,path

from . import views

urlpatterns = [
	path('login/',views.login,name='login_instructor'),
	path('newinstructor/',views.newinstructor),
    path('', views.index),
    path('logout/',views.logout),
    path('new_exam',views.new_exam,name='new_exam'),
    path('edit_exam/<int:exam_id>',views.edit_exam,name='edit_exam'),
    path('edit_question/<int:question_id>',views.edit_question,name='edit_question'),
    path('new_question/<int:exam_id>',views.new_question,name='new_question'),
    path('exam/<int:exam_id>',views.show_exam,name='show_exam'),
    path('topics_in_qb/',views.topics_in_qb,name='topics_in_qb'),
]
