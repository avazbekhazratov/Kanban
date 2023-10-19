from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from kanban.models.core import BoardMember, SubTask
from kanban.serializers import BoardMemberSerializer, SubTaskSerializer
from rest_framework import status


class SubTaskView(GenericAPIView):
    serializer_class = SubTaskSerializer

    def get(self, request, pk=None):
        if pk:
            board = SubTask.objects.filter(id=pk).first()
            if board:
                serializer = self.get_serializer(board).data
                return Response({"succes": serializer}, status=status.HTTP_200_OK)
            return Response({"Error": "Not Found"}, status=status.HTTP_404_NOT_FOUND)
        Subman = SubTask.objects.all()
        serializer = self.get_serializer(Subman, many=True).data
        return Response({'Success': serializer}, status=status.HTTP_200_OK)



    def post(self, request):
        data = request.data
        if "title" not in data or not data['title']:
            return Response({"Error": "Fields are empty"}, status=status.HTTP_404_NOT_FOUND)
        if "task_item" not in data or not data['task_item']:
            return Response({"Error": "Fields are empty"}, status=status.HTTP_404_NOT_FOUND)
    def put(self, request, pk):
        data = request.data
        if "title" not in data or not data['title']:
            return Response({"error": "empty"})
        Subman = SubTask.objects.filter(pk=pk).first()
        if Subman:
            serializer = self.get_serializer(data=data, instance=Subman)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'Success': "you have edited"}, status=status.HTTP_200_OK)
        return Response({'Error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        Subman = SubTask.objects.filter(id=pk).first()
        if Subman:
            Subman.delete()
            return Response({"Success": "Successfully deleted"}, status=status.HTTP_200_OK)
        return Response({"Error": "Data not found"}, status=status.HTTP_404_NOT_FOUND)

