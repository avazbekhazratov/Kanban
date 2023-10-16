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
        fields = '__all__'


class SubTaskSerializer(ModelSerializer):
    class Meta:
        model = SubTask
        fields = '__all__'


class BoardMemberSerializer(ModelSerializer):
    class Meta:
        model = BoardMember
        fields = '__all__'
