from django.contrib import admin
from . models import Instructor, Courses, Exam, Question

# Register your models here.

admin.site.register(Instructor)
admin.site.register(Courses)
admin.site.register(Exam)
admin.site.register(Question)
