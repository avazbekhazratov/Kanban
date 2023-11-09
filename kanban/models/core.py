from django.db import models

from kanban.models.user import User


class Board(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return f"{self.title}"


class TaskCondition(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=128)
    desc = models.TextField()

    def __str__(self):
        return f"{self.title}"


class TaskItem(models.Model):
    title = models.CharField(max_length=2000)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    task_condition = models.ForeignKey(TaskCondition, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class SubTask(models.Model):
    title = models.CharField(max_length=256)
    task_item = models.ForeignKey(TaskItem, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class BoardMember(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    member = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.board.title} | {self.member.username}"
