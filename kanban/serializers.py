from rest_framework import serializers
from .models.core import Board, TaskCondition, TaskItem, SubTask, BoardMember


class SubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = '__all__'


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = '__all__'

    def to_representation(self, instance):
        res = super().to_representation(instance)
        res['creator'] = {
            "id": instance.creator.id,
            "phone": instance.creator.phone,
            "username": instance.creator.username
        }
        return res

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['creator'] = user
        board = Board.objects.select_related('creator').filter(creator=user)
        if board.first():
            raise serializers.ValidationError("Board's title is unique")
        board = Board.objects.create(**validated_data)
        return board


class TaskItemSerializer(serializers.ModelSerializer):
    sub_task = SubTaskSerializer(many=True, read_only=True)

    class Meta:
        model = TaskItem
        fields = '__all__'

    def to_representation(self, instance):
        res = super().to_representation(instance)
        res['creator'] = {
            "id": instance.creator.id,
            "phone": instance.creator.phone,
            "username": instance.creator.username
        }
        res['task_condition'] = {
            "title": instance.task_condition.title,
            "creator": instance.task_condition.creator.phone,
            "board": instance.task_condition.board.title
        }
        return res

    def create(self, validated_data):
        user = self.context['request'].user
        task_condition = validated_data.get('task_condition')

        if task_condition.creator == user:
            validated_data['creator'] = user
            task_item = TaskItem.objects.create(**validated_data)
            return task_item
        else:
            raise serializers.ValidationError("You can only link to your own Tasks !!!")


class TaskConditionSerializer(serializers.ModelSerializer):
    task_item = TaskItemSerializer(many=True, read_only=True)

    class Meta:
        model = TaskCondition
        fields = '__all__'

    def to_representation(self, instance):
        res = super().to_representation(instance)
        res['creator'] = {
            "phone": instance.creator.phone,
            "username": instance.creator.username
        }
        return res

    def create(self, validated_data):
        user = self.context['request'].user
        linked_board = validated_data.get('board')

        if linked_board.creator == user:
            validated_data['creator'] = user
            task_condition = TaskCondition.objects.create(**validated_data)
            return task_condition
        else:
            raise serializers.ValidationError("You can only link to your own boards !!!")


class BoardMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardMember
        fields = '__all__'

    def create(self, validated_data):
        user = self.context['request'].user
        board = validated_data.get("board")
        member = validated_data['member']
        board_members = BoardMember.objects.filter(board_id=board.id)

        for board_member in board_members:
            if board_member.member == member:
                raise serializers.ValidationError("User exists")

        if member != user:
            board_member = BoardMember.objects.create(**validated_data)
        else:
            raise serializers.ValidationError("Error saving user")
