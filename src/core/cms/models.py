from django.db import models
from django.contrib.auth.models import User
class Tag(models.Model):
    name = models.CharField(max_length=100)

class Category(models.Model):
    name = models.CharField(max_length=100)
    parentcategory = models.ForeignKey('self', on_delete=models.PROTECT)

class Object_Type(models.Model):
    name = models.CharField(max_length=100)

class Object(models.Model):
    objectlink = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.ForeignKey(Object_Type, on_delete=models.CASCADE)

class ShortCode(models.Model):
    name = models.CharField(max_length=100)
    content = models.TextField
    ispage = models.BooleanField
    date_of_creation = models.DateField
    last_update = models.DateTimeField
    user =models.ForeignKey(User, on_delete=models.CASCADE)

class ShortCode_Parameter(models.Model):
    key = models.CharField(max_length=100)
    value = models.TextField
    shortcode = models.ForeignKey(ShortCode, on_delete=models.CASCADE)