from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from kanban.models.core import TaskItem
from kanban.serializers import TaskItemSerializer
from rest_framework import status


class TaskItemView(GenericAPIView):
    serializer_class = TaskItemSerializer

    def get(self, request, pk=None):
        if pk:
            task = TaskItem.objects.filter(id=pk).first()
            if task:
                serializer = self.get_serializer(task).data
                return Response({"succes": serializer}, status=status.HTTP_200_OK)
            return Response({"Error": "Not Found"}, status=status.HTTP_404_NOT_FOUND)
        taskMem = TaskItem.objects.all()
        serializer = self.get_serializer(taskMem, many=True).data
        return Response({'Success': serializer}, status=status.HTTP_200_OK)



    def post(self, request):
        data = request.data
        if "title" not in data or not data['title']:
            return Response({"Error": "Fields are empty"}, status=status.HTTP_404_NOT_FOUND)
        if "creator" not in data or not data['creator']:
            return Response({"Error": "Fields are empty"}, status=status.HTTP_404_NOT_FOUND)
        if "task_condition" not in data or not data['task_condition']:
            return Response({"Error": "Fields are empty"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'Success': "you have added"})
    def put(self, request, pk):
        data = request.data
        if "title" not in data or not data['title']:
            return Response({"error": "empty"})
        if "creator" not in data or not data['creator']:
            return Response({"Error": "Fields are empty"}, status=status.HTTP_404_NOT_FOUND)
        if "task_condition" not in data or not data['task_condition']:
            return Response({"Error": "Fields are empty"}, status=status.HTTP_404_NOT_FOUND)

        BoardMem = TaskItem.objects.filter(pk=pk).first()
        if BoardMem:
            serializer = self.get_serializer(data=data, instance=BoardMem)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'Success': "you have edited"}, status=status.HTTP_200_OK)
        return Response({'Error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        BoardMem = TaskItem.objects.filter(id=pk).first()
        if BoardMem:
            BoardMem.delete()
            return Response({"Success": "Successfully deleted"}, status=status.HTTP_200_OK)
        return Response({"Error": "Data not found"}, status=status.HTTP_404_NOT_FOUND)

