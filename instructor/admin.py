from django.contrib import admin
from . models import Exam, Question, Question_Bank, Topic

# Register your models here.

#admin.site.register(Courses)
admin.site.register(Exam)
admin.site.register(Question)
admin.site.register(Question_Bank)
admin.site.register(Topic)
