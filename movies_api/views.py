from django.shortcuts import render

from rest_framework.response import Response
from rest_framework import status, generics
from movies_api.models import MovieModel
from movies_api.serializers import MovieSerializer
from roles_api.models import RoleModel
from roles_api.serializers import RoleSerializer
from actors_api.serializers import ActorSerializer
from actors_api.models import ActorModel
import math
from datetime import datetime


class Movies(generics.GenericAPIView):
    movie_ser = MovieSerializer
    queryset = MovieModel.objects.all()

    def get(self, request):
        page_num = int(request.GET.get("page", 1))
        limit_num = int(request.GET.get("limit", 10))
        start_num = (page_num - 1) * limit_num
        end_num = limit_num * page_num
        search_param = request.GET.get("search")
        movies = MovieModel.objects.all()
        total_movies = movies.count()
        if search_param:
            movies = movies.filter(title__icontains=search_param)
        serializer = self.movie_ser(
            movies[start_num:end_num], many=True)
        return Response({
            "status": "success",
            "total": total_movies,
            "page": page_num,
            "last_page": math.ceil(total_movies / limit_num),
            "movies": serializer.data
        })

    def post(self, request):
        serializer = self.movie_ser(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "movie": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class MovieDetail(generics.GenericAPIView):
    queryset = MovieModel.objects.all()
    movie_ser = MovieSerializer

    def get_movie(self, pk):
        try:
            return MovieModel.objects.get(pk=pk)
        except:
            return None

    def get(self, request, pk):
        movie = self.get_movie(pk=pk)
        if movie == None:
            return Response({"status": "fail", "message": f"Movie with Id: {pk} not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.movie_ser(movie)
        return Response({"status": "success", "movie": serializer.data})

    def patch(self, request, pk):
        movie = self.get_movie(pk)
        if movie == None:
            return Response({"status": "fail", "message": f"Movie with Id: {pk} not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.movie_ser(
            movie, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "movie": serializer.data})
        return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        movie = self.get_movie(pk)
        if movie == None:
            return Response({"status": "fail", "message": f"Movie with Id: {pk} not found"}, status=status.HTTP_404_NOT_FOUND)

        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


from django.db.models import OuterRef, Count, CharField

class MoviesByActors(generics.ListCreateAPIView):
    serializer_class = MovieSerializer

    def actor_count(self, obj):
        return obj.actor_count

    def get_queryset(self):
        query = MovieModel.objects.annotate(
            actor_count=Count(
                RoleModel.objects.filter(
                    movie=OuterRef('pk')
                ).values('actor').distinct(),
                distinct=True
            )
        ).order_by('-actor_count')

        print(query.query)

        return query

class MoviesByRating(generics.ListCreateAPIView):
    serializer_class = MovieSerializer

    def get_queryset(self):
        query = MovieModel.objects.all().order_by('-rating')

        print(query.query)

        return query