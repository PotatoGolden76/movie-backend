from django.urls import path
from movies_api.views import Movies, MovieDetail

urlpatterns = [
    path('', Movies.as_view()),
    path('<str:pk>', MovieDetail.as_view())
]