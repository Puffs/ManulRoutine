from django.db import models
from boardapp.models import Column

class Task(models.Model):
    name = models.CharField(max_length=200)
    typ = models.CharField(max_length=10, blank=True, null=True)
    column = models.ForeignKey(Column, on_delete=models.CASCADE)
