from django.shortcuts import render

from rest_framework.response import Response
from rest_framework import status, generics
from directors_api.models import DirectorModel
from directors_api.serializers import DirectorSerializer
import math
from datetime import datetime


class Directors(generics.GenericAPIView):
    serializer_class = DirectorSerializer
    queryset = DirectorModel.objects.all()

    def get(self, request):
        page_num = int(request.GET.get("page", 1))
        limit_num = int(request.GET.get("limit", 10))
        start_num = (page_num - 1) * limit_num
        end_num = limit_num * page_num
        search_param = request.GET.get("search")
        directors = DirectorModel.objects.all()
        total_directors = directors.count()
        if search_param:
            directors = directors.filter(title__icontains=search_param)
        serializer = self.serializer_class(
            directors[start_num:end_num], many=True)
        return Response({
            "status": "success",
            "total": total_directors,
            "page": page_num,
            "last_page": math.ceil(total_directors / limit_num),
            "directors": serializer.data
        })

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "director": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class DirectorDetail(generics.GenericAPIView):
    queryset = DirectorModel.objects.all()
    serializer_class = DirectorSerializer

    def get_director(self, pk):
        try:
            return DirectorModel.objects.get(pk=pk)
        except:
            return None

    def get(self, request, pk):
        director = self.get_director(pk=pk)
        if director == None:
            return Response({"status": "fail", "message": f"Director with Id: {pk} not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(director)
        return Response({"status": "success", "director": serializer.data})

    def patch(self, request, pk):
        director = self.get_director(pk)
        if director == None:
            return Response({"status": "fail", "message": f"Director with Id: {pk} not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(
            director, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "director": serializer.data})
        return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        director = self.get_director(pk)
        if director == None:
            return Response({"status": "fail", "message": f"Director with Id: {pk} not found"}, status=status.HTTP_404_NOT_FOUND)

        director.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class DirectorFilter(generics.ListAPIView):
    serializer_class = DirectorSerializer

    def get_queryset(self):
        return DirectorModel.objects.filter(name__contains=self.kwargs['val'])
