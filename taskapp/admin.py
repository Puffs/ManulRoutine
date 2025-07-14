from django.contrib import admin
from taskapp.models import Task

class TaskAdmin(admin.ModelAdmin):
    pass

admin.site.register(Task, TaskAdmin)
