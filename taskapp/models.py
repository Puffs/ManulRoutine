from django.db import models
from boardapp.models import Column
from datetime import datetime

class Task(models.Model):
    name = models.CharField(max_length=200)
    typ = models.CharField(max_length=10, blank=True, null=True)
    order = models.IntegerField(blank=True, null=True)
    column = models.ForeignKey(Column, on_delete=models.CASCADE)

class Comment(models.Model):
    text = models.TextField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    date = models.DateTimeField(default=datetime.now())