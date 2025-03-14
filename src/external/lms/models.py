from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField
    creationdate = models.DateField
    lastupdate = models.DateTimeField
    teacher = models.ForeignKey(User, on_delete= models.CASCADE)

class Grade(models.Model):
    course = models.ForeignKey(Course, on_delete= models.CASCADE)
    related = models.DateField
    lastupdate = models.DateTimeField
    student = models.ForeignKey(User, on_delete= models.CASCADE)

class Theme(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField
    creationdate = models.DateField
    lastupdate = models.DateTimeField
    course = models.ForeignKey(Course, on_delete= models.CASCADE)

class Lesson(models.Model):
    class LessonType(models.TextChoices):
        video = 'V'
        conference ='C'
        lecture = 'L'
    name = models.CharField(max_length=100)
    description = models.TextField
    creationdate = models.DateField
    lastupdate = models.DateTimeField    
    lessontype = models.CharField(max_length=40,choices=LessonType.choices, default=LessonType.lecture)
    content = models.BinaryField 
    theme = models.ForeignKey(Theme, on_delete= models.CASCADE)

class Test(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField
    creationdate = models.DateField
    lastupdate = models.DateTimeField
    lesson = models.ForeignKey(Lesson, on_delete= models.CASCADE)
    timelimit = models.IntegerField
    class TestType(models.TextChoices):
        close = 'C'
        game = 'G'
        open = 'O'
    type = models.CharField(max_length=100,choices=TestType, default= TestType.close)   
    title = models.CharField(max_length=255)

class Question(models.Model):
    text= models.TextField
    points = models.IntegerField
    lastupdate = models.DateTimeField
    correctanswer = models.TextField
    class QuestionType(models.TextChoices):
        single = 'S'
        open = 'O'
    type = models.CharField(max_length=2, choices=QuestionType, default=QuestionType.single)
    test = models.ForeignKey(Test, on_delete= models.CASCADE)

class UserAnswer(models.Model):
    answer = models.TextField
    iscorrect = models.BooleanField
    Student = models.ForeignKey(User, on_delete= models.CASCADE)
    Question = models.ForeignKey(Question, on_delete= models.CASCADE)

class Assignment(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField
    deadline = models.DateField
    creationdate = models.DateField
    lastupdate = models.DateTimeField
    lesson = models.ForeignKey(Lesson, on_delete= models.CASCADE)

class SubmittedAssignment(models.Model):
    submittedassignment = models.BinaryField
    comment = models.TextField 
    grade = models.IntegerField
    dateofsubmit = models.DateField
    Student = models.ForeignKey(User, on_delete= models.CASCADE)
    Assignment = models.ForeignKey(Assignment, on_delete= models.CASCADE)
