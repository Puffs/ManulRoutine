from django.db import models
from userapp.models import CustomUser


def background_image_path(instance, filename):
    return 'board/' + str(instance.id) + '/background_image/' + str(filename)

class Board(models.Model):
    name = models.CharField(max_length=30)
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    user_list = models.ManyToManyField(CustomUser, related_name='users', blank=True)
    background_image = models.ImageField(blank=True, null=True, upload_to=background_image_path)
    
class Column(models.Model):
    name = models.CharField(max_length=30)
    order = models.IntegerField(blank=True, null=True)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)