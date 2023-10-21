from rest_framework.serializers import ModelSerializer
from .models.core import Board, TaskCondition, TaskItem, SubTask, BoardMember


class BoardSerializer(ModelSerializer):
    class Meta:
        model = Board
        fields = '__all__'


class TaskConditionSerializer(ModelSerializer):
    class Meta:
        model = TaskCondition
        fields = '__all__'


class TaskItemSerializer(ModelSerializer):
    class Meta:
        model = TaskItem
        fields = ('id', 'title', 'creator', 'task_condition')

    def to_representation(self, instance):
        res = super().to_representation(instance)
        if instance.creator:
            res['creator'] = {
                "phone": instance.creator.phone,
                "username": instance.creator.username
            }
        if instance.task_condition:
            res['task_condition'] = {
                "title": instance.task_condition.title,
                "creator": instance.task_condition.creator.phone,
                "board": instance.task_condition.board.title,
            }
        return res

class SubTaskSerializer(ModelSerializer):
    class Meta:
        model = SubTask
        fields = '__all__'


class BoardMemberSerializer(ModelSerializer):
    class Meta:
        model = BoardMember
        fields = '__all__'
