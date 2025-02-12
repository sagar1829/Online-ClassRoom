from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.conf import settings


# Create your models here.

class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)


class Course_master(models.Model):
    course_name = models.CharField(max_length=200, null=True, blank=True)
    course_duration = models.CharField(max_length=20, null=True, blank=True)
    total_semester = models.IntegerField(null=True, default=6)

    def __str__(self):
        return self.course_name


class Subject_master(models.Model):
    course = models.ForeignKey(Course_master, on_delete=models.CASCADE)
    subject_name = models.CharField(max_length=200, null=True, blank=True)
    semester = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.subject_name + " | sem ("+str(self.semester)+")"


class Student(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name='Student')
    name = models.CharField(max_length=250)
    std_course = models.ForeignKey(
        Course_master, on_delete=models.CASCADE, null=True, blank=True)
    sem = models.CharField(max_length=50, default=1, null=True, blank=True)
    email = models.EmailField(max_length=254)
    phone = models.IntegerField()
    student_profile_pic = models.ImageField(
        upload_to="classroom/student_profile_pic", blank=True)

    def get_absolute_url(self):
        return reverse('classroom:student_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name

    # class Meta:
    #     ordering = ['roll_no']


class Teacher(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name='Teacher')
    name = models.CharField(max_length=250)
    subject_name = models.CharField(max_length=200, blank=True)
    # subject_name = models.ForeignKey(Subject_master,on_delete=models.CASCADE)
    email = models.EmailField(max_length=254)
    phone = models.IntegerField()
    teacher_profile_pic = models.ImageField(
        upload_to="classroom/teacher_profile_pic", blank=True)
    class_students = models.ManyToManyField(Student, through="StudentsInClass")

    def get_absolute_url(self):
        return reverse('classroom:teacher_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name


class Teacher_subject_allocation(models.Model):
    subject = models.ForeignKey(Subject_master, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)


class StudentMarks(models.Model):
    teacher = models.ForeignKey(
        Teacher, related_name='given_marks', on_delete=models.CASCADE)
    student = models.ForeignKey(
        Student, related_name="marks", on_delete=models.CASCADE)
    subject_name = models.CharField(max_length=250)
    submission_id = models.CharField(max_length=20, null=True, blank=True)
    marks_obtained = models.IntegerField()
    maximum_marks = models.IntegerField()

    def __str__(self):
        return self.subject_name


class StudentsInClass(models.Model):
    teacher = models.ForeignKey(
        Teacher, related_name="class_teacher", on_delete=models.CASCADE)
    student = models.ForeignKey(
        Student, related_name="user_student_name", on_delete=models.CASCADE)

    def __str__(self):
        return self.student.name

    class Meta:
        unique_together = ('teacher', 'student')


class MessageToTeacher(models.Model):
    student = models.ForeignKey(
        Student, related_name='student', on_delete=models.CASCADE)
    teacher = models.ForeignKey(
        Teacher, related_name='messages', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    message = models.TextField()
    message_html = models.TextField(editable=False)

    def __str__(    self):
        return self.message

    # def save(self,*args,**kwargs):
    #     self.message_html = misaka.html(self.message)
    #     super().save(*args,**kwargs)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['student', 'message']


class ClassNotice(models.Model):
    teacher = models.ForeignKey(
        Teacher, related_name='teacher', on_delete=models.CASCADE)
    students = models.ManyToManyField(Student, related_name='class_notice')
    created_at = models.DateTimeField(auto_now=True)
    message = models.TextField()
    message_html = models.TextField(editable=False)

    def __str__(self):
        return self.message

    # def save(self,*args,**kwargs):
    #     self.message_html = misaka.html(self.message)
    #     super().save(*args,**kwargs)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['teacher', 'message']


class ClassAssignment(models.Model):
    student = models.ManyToManyField(
        Student, related_name='student_assignment')
    teacher = models.ForeignKey(
        Teacher, related_name='teacher_assignment', on_delete=models.CASCADE)
    ass_sub = models.ForeignKey(
        Subject_master, null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    due_date = models.DateField(null=True, blank=True)
    assignment_name = models.CharField(max_length=250)
    assignment = models.FileField(upload_to='assignments')
    maxMark = models.IntegerField(default=20, null=True, blank=True)

    def __str__(self):
        return self.assignment_name

    class Meta:
        ordering = ['-created_at']


class SubmitAssignment(models.Model):
    student = models.ForeignKey(
        Student, related_name='student_submit', on_delete=models.CASCADE)
    teacher = models.ForeignKey(
        Teacher, related_name='teacher_submit', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    submitted_assignment = models.ForeignKey(
        ClassAssignment, related_name='submission_for_assignment', on_delete=models.CASCADE)
    submit = models.FileField(upload_to='Submission')
    temp_marks = models.CharField(max_length=5, null=True, blank=True)
    is_marked = models.BooleanField(default=0, null=True, blank=True)

    def __str__(self):
        return "Submitted"+str(self.submitted_assignment.assignment_name)

    class Meta:
        ordering = ['-created_at']
