from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
# Register your models here.


admin.site.register(User,UserAdmin)
admin.site.register(Student)
admin.site.register(StudentMarks)
admin.site.register(Teacher)
admin.site.register(StudentsInClass)


# Course
class CourseMasterAdmin(admin.ModelAdmin):
    list_display =('course_name','course_duration','total_semester')
admin.site.register(Course_master,CourseMasterAdmin)


# Subject
class SubjectMasterAdmin(admin.ModelAdmin):
    list_display = ('course', 'subject_name', 'semester')
admin.site.register(Subject_master,SubjectMasterAdmin)


# Teacher allocation
class TeacherSubAdmin(admin.ModelAdmin):
    list_display =('subject','teacher')

admin.site.register(Teacher_subject_allocation,TeacherSubAdmin)

admin.site.register(MessageToTeacher)

admin.site.register(ClassNotice )
admin.site.register(SubmitAssignment)
admin.site.register(ClassAssignment)
