from django.contrib import admin
from boardapp.models import Board, Column


class BoardAdmin(admin.ModelAdmin):
    pass

class ColumnAdmin(admin.ModelAdmin):
    pass

admin.site.register(Board, BoardAdmin)
admin.site.register(Column, ColumnAdmin)