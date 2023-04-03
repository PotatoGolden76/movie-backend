from django.urls import path
from movies_api.views import Movies, MovieDetail, MoviesByActors, MoviesByRating

urlpatterns = [
    path('', Movies.as_view()),
    path('stat', MoviesByActors.as_view()),
    path('rating', MoviesByRating.as_view()),
    path('<str:pk>', MovieDetail.as_view())
    
]