from base.helper import BearerAuth
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from kanban.models.core import BoardMember
from kanban.serializers import BoardMemberSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

class BoardMemberView(GenericAPIView):
    serializer_class = BoardMemberSerializer
    permission_classes = IsAuthenticated,
    authentication_classes = BearerAuth,

    def get(self, request, pk=None):
        if pk:
            board = BoardMember.objects.filter(id=pk).first()
            if board:
                serializer = self.get_serializer(board).data
                return Response({"succes": serializer}, status=status.HTTP_200_OK)
            return Response({"Error": "Not Found"}, status=status.HTTP_404_NOT_FOUND)
        BoardMem = BoardMember.objects.all()
        serializer = self.get_serializer(BoardMem, many=True).data
        return Response({'Success': serializer}, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        if "board" not in data or not data['board']:
            return Response({"Error": "Fields are empty"}, status=status.HTTP_404_NOT_FOUND)
        if "member" not in data or not data['member']:
            return Response({"Error": "Fields are empty"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'Success': "you have added"})

    def put(self, request, pk):
        data = request.data
        if "board" not in data or not data['board']:
            return Response({"Error": "Fields are empty"}, status=status.HTTP_404_NOT_FOUND)
        if "member" not in data or not data['member']:
            return Response({"Error": "Fields are empty"}, status=status.HTTP_404_NOT_FOUND)

        BoardMem = BoardMember.objects.filter(pk=pk).first()
        if BoardMem:
            serializer = self.get_serializer(data=data, instance=BoardMem)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'Success': "you have edited"}, status=status.HTTP_200_OK)
        return Response({'Error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        BoardMem = BoardMember.objects.filter(id=pk).first()
        if BoardMem:
            BoardMem.delete()
            return Response({"Success": "Successfully deleted"}, status=status.HTTP_200_OK)
        return Response({"Error": "Data not found"}, status=status.HTTP_404_NOT_FOUND)
