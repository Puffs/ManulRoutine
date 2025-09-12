from django.db import models
from boardapp.models import Column
from userapp.models import CustomUser
from datetime import datetime

class Task(models.Model):
    name = models.CharField(max_length=200)
    typ = models.CharField(max_length=10, blank=True, null=True)
    order = models.IntegerField(blank=True, null=True)
    column = models.ForeignKey(Column, on_delete=models.CASCADE)
    executor = models.ManyToManyField(CustomUser, related_name='tasks', blank=True)

class Comment(models.Model):
    text = models.TextField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    date = models.DateTimeField(default=datetime.now())
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)