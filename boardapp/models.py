from django.db import models


class Board(models.Model):
    name = models.CharField(max_length=30)


class Column(models.Model):
    name = models.CharField(max_length=30)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)