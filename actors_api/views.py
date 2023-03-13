from django.shortcuts import render

from rest_framework.response import Response
from rest_framework import status, generics
from actors_api.models import ActorModel
from actors_api.serializers import ActorSerializer
import math
from datetime import datetime


class Actors(generics.GenericAPIView):
    serializer_class = ActorSerializer
    queryset = ActorModel.objects.all()

    def get(self, request):
        page_num = int(request.GET.get("page", 1))
        limit_num = int(request.GET.get("limit", 10))
        start_num = (page_num - 1) * limit_num
        end_num = limit_num * page_num
        search_param = request.GET.get("search")
        actors = ActorModel.objects.all()
        total_actors = actors.count()
        if search_param:
            actors = actors.filter(title__icontains=search_param)
        serializer = self.serializer_class(
            actors[start_num:end_num], many=True)
        return Response({
            "status": "success",
            "total": total_actors,
            "page": page_num,
            "last_page": math.ceil(total_actors / limit_num),
            "actors": serializer.data
        })

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "actor": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class ActorDetail(generics.GenericAPIView):
    queryset = ActorModel.objects.all()
    serializer_class = ActorSerializer

    def get_actor(self, pk):
        try:
            return ActorModel.objects.get(pk=pk)
        except:
            return None

    def get(self, request, pk):
        actor = self.get_actor(pk=pk)
        if actor == None:
            return Response({"status": "fail", "message": f"actor with Id: {pk} not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(actor)
        return Response({"status": "success", "actor": serializer.data})

    def patch(self, request, pk):
        actor = self.get_actor(pk)
        if actor == None:
            return Response({"status": "fail", "message": f"actor with Id: {pk} not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(
            actor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "actor": serializer.data})
        return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        actor = self.get_actor(pk)
        if actor == None:
            return Response({"status": "fail", "message": f"actor with Id: {pk} not found"}, status=status.HTTP_404_NOT_FOUND)

        actor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
