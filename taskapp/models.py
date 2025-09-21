from django.db import models
from boardapp.models import Column
from userapp.models import CustomUser
from datetime import datetime
from django.db.models.signals import post_delete
from django.dispatch import receiver
import os

def comment_img_path(instance, filename):
    return 'user/' + str(instance.author.id) + '/comment/img/' + str(filename)

def comment_file_path(instance, filename):
    return 'user/' + str(instance.author.id) + '/comment/file/' + str(filename)

class Task(models.Model):
    name = models.CharField(max_length=200)
    typ = models.CharField(max_length=10, blank=True, null=True)
    order = models.IntegerField(blank=True, null=True)
    column = models.ForeignKey(Column, on_delete=models.CASCADE)
    executor = models.ManyToManyField(CustomUser, related_name='tasks', blank=True)

class Comment(models.Model):
    text = models.TextField(blank=True, null=True)
    img_file = models.ImageField(blank=True, null=True, upload_to=comment_img_path)
    data = models.FileField(blank=True, null=True, upload_to=comment_file_path)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    date = models.DateTimeField(default=datetime.now())
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)


@receiver(post_delete, sender=Comment)
def delete_file_on_model_delete(sender, instance, **kwargs):
    if instance.img_file:
        if os.path.isfile(instance.img_file.path):
            os.remove(instance.img_file.path)
    if instance.data:
        if os.path.isfile(instance.data.path):
            os.remove(instance.data.path)