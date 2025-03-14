from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    name = models.CharField(max_length=100)
    dateofcreation = models.DateField
    creator = models.ForeignKey(User, on_delete= models.CASCADE)

class User_Project(models.Model):
    project = models.ForeignKey(Project, on_delete= models.CASCADE)
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    isnew = models.BooleanField

class Section(models.Model):
    name = models.CharField(max_length=100)
    Project = models.ForeignKey(Project, on_delete= models.CASCADE)

class Task(models.Model):
    text = models.TextField
    isdone = models.BooleanField
    description = models.TextField
    dateofcreation = models.DateField
    deadline = models.DateField
    priority = models.IntegerField
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    parenttask = models.ForeignKey('self', on_delete= models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
