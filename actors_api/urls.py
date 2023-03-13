from actors_api.views import Actors, ActorDetail
from django.urls import path

urlpatterns = [
    path('', Actors.as_view()),
    path('<str:pk>', ActorDetail.as_view())
]