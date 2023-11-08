from base.helper import BearerAuth
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from kanban.models.core import SubTask
from kanban.serializers import SubTaskSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

class SubTaskView(GenericAPIView):
    serializer_class = SubTaskSerializer
    permission_classes = IsAuthenticated,
    authentication_classes = BearerAuth,

    def get(self, request, pk=None):
        if pk:
            subtasks = SubTask.objects.filter(id=pk).first()
            if subtasks:
                serializer = self.get_serializer(subtasks).data
                return Response({"succes": serializer}, status=status.HTTP_200_OK)
            return Response({"Error": "Not Found"}, status=status.HTTP_404_NOT_FOUND)
        subtasks = SubTask.objects.all()
        serializer = self.get_serializer(subtasks, many=True).data
        return Response({'Success': serializer}, status=status.HTTP_200_OK)


    def post(self, request):
        data = request.data
        if "title" not in data or not data['title']:
            return Response({"Error": "Fields are empty"}, status=status.HTTP_404_NOT_FOUND)
        if "task_item" not in data or not data['task_item']:
            return Response({"Error": "Fields are empty"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'Success': "you have added"})

    def put(self, request, pk):
        data = request.data
        if "title" not in data or not data['title']:
            return Response({"error": "empty"})
        if "task_item" not in data or not data['task_item']:
            return Response({"Error": "Fields are empty"}, status=status.HTTP_404_NOT_FOUND)

        subtasks = SubTask.objects.filter(pk=pk).first()
        if subtasks:
            serializer = self.get_serializer(data=data, instance=subtasks)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'Success': "you have edited"}, status=status.HTTP_200_OK)
        return Response({'Error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        subtasks = SubTask.objects.filter(id=pk).first()
        if subtasks:
            subtasks.delete()
            return Response({"Success": "Successfully deleted"}, status=status.HTTP_200_OK)
        return Response({"Error": "Data not found"}, status=status.HTTP_404_NOT_FOUND)

