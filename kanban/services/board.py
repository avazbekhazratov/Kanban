from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from base.helper import BearerAuth
from rest_framework.permissions import IsAuthenticated
from kanban.serializers import BoardSerializer
from kanban.models.core import Board


class BoardView(GenericAPIView):
    serializer_class = BoardSerializer
    permission_classes = IsAuthenticated,
    authentication_classes = BearerAuth,
    def get(self, request, pk=None):
        try:
            if pk:
                board = Board.objects.filter(id=pk).first()
                if board:
                    serializer = BoardSerializer(board).data
                    return Response({"success": serializer})
                return Response({"error": "Board not found"})
            board = Board.objects.all()
            serializer = BoardSerializer(board, many=True).data
            return Response({'success': serializer})
        except Exception as e:
            return Response({"error": str(e)})



    def post(self, request):
        data = request.data
        if "title" not in data or not data['title']:
            return Response({"error": "title"})

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'Success': "you have added"})

    def put(self, request, pk):
        data = request.data
        if "title" not in data or not data['title']:
            return Response({"error": "title"})
        if "creator" not in data or not data['creator']:
            return Response({"error": "creator"})

        bosa = Board.objects.filter(pk=pk).first()
        if bosa:
            serializer = self.get_serializer(data=data, instance=bosa)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'Success': "you have edited"})
        return Response({'Error': 'Not found'})

    def delete(self, request, pk):
        data = request.data
        board = Board.objects.filter(id=pk).first()
        if board:
            board.delete()
            return Response({"Success": "Successfully deleted"})
        return Response({"Error": "Data not found"})
