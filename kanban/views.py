from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .serializers import BoardSerializer
from .models.core import Board


class Items(GenericAPIView):
    serializer_class = BoardSerializer

    def get(self, request):
        board = Board.objects.all()
        serializer = self.get_serializer(board, many=True).data
        return Response({'Success': serializer})

    def post(self, request):
        data = request.data
        if "title" not in data or not data['title']:
            return Response({"error": "empty"})

        if "creator" not in data or not data['creator']:
            return Response({"error": "empty"})

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'Success': "you have added"})
