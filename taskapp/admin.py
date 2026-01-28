from django.contrib import admin
from taskapp.models import Task, Comment


class TaskAdmin(admin.ModelAdmin):
    pass

class CommentAdmin(admin.ModelAdmin):
    pass

admin.site.register(Task, TaskAdmin)
admin.site.register(Comment, TaskAdmin)
