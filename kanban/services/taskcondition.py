from rest_framework import status
from base.helper import BearerAuth
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from kanban.serializers import TaskConditionSerializer
from kanban.models.core import TaskCondition


class TaskConditionView(GenericAPIView):
    serializer_class = TaskConditionSerializer
    permission_classes = IsAuthenticated,
    authentication_classes = BearerAuth,

    def get(self, request, pk=None):
        try:
            if pk:
                task_condition = TaskCondition.objects.filter(id=pk).first()
                if task_condition:
                    serializer = self.get_serializer(task_condition).data
                    return Response({"success": serializer})
                return Response({"error": "Task Condition not found"}, status=status.HTTP_404_NOT_FOUND)
            else:
                task_conditions = TaskCondition.objects.all()
                serializer = self.get_serializer(task_conditions, many=True).data
                return Response({'Success': serializer})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        data = request.data
        if "board" not in data or not data['board']:
            return Response({"error": "empty"})

        if "title" not in data or not data['title']:
            return Response({"error": "empty"})

        if "desc" not in data or not data['desc']:
            return Response({"error": "empty"})

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'Success': "you have added"})

    def put(self, request, pk):
        data = request.data

        if "board" not in data or not data['board']:
            return Response({"error": "empty"})

        if "title" not in data or not data['title']:
            return Response({"error": "empty"})

        if "desc" not in data or not data['desc']:
            return Response({"error": "empty"})

        bosa = TaskCondition.objects.filter(pk=pk).first()
        if bosa:
            serializer = self.get_serializer(data=data, instance=bosa)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'Success': "you have edited"})
        return Response({'Error': 'Not found'})

    def delete(self, request, pk):
        data = request.data
        board = TaskCondition.objects.filter(id=pk).first()
        if board:
            board.delete()
            return Response({"Success": "Successfully deleted"})
        return Response({"Error": "Data not found"})
