from django.db import models
from django.contrib.auth.models import AbstractUser


def user_path(instance, filename):
    return 'user/' + str(instance.id) + '/avatar/' + str(filename)

class CustomUser(AbstractUser):
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    avatar = models.ImageField(blank=True, null=True, upload_to=user_path)