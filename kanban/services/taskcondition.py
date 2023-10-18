from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from kanban.serializers import TaskConditionSerializer
from kanban.models.core import TaskCondition, TaskItem, SubTask, BoardMember


class TaskCondt(GenericAPIView):
    serializer_class = TaskConditionSerializer

    def get(self, request, pk=None):
        try:
            if pk:
                board = TaskCondition.objects.filter(id=pk).first()
                if board:
                    serializer = self.get_serializer(board).data
                    return Response({"succes": serializer})
                return Response({"error"})
            board = TaskCondition.objects.all()
            serializer = self.get_serializer(board, many=True).data
            return Response({'Success': serializer})
        except:
            return 0

    def post(self, request):
        data = request.data
        if "board" not in data or not data['board']:
            return Response({"error": "empty"})

        if "creator" not in data or not data['creator']:
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

        if "creator" not in data or not data['creator']:
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
