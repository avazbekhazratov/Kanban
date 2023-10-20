from django.contrib import admin
from .models.core import Board, TaskCondition, TaskItem, SubTask, BoardMember


admin.site.register(Board)
admin.site.register(TaskCondition)
admin.site.register(TaskItem)
admin.site.register(SubTask)
admin.site.register(BoardMember)
