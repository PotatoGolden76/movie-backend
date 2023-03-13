from directors_api.views import Directors, DirectorDetail
from django.urls import path

urlpatterns = [
    path('', Directors.as_view()),
    path('<str:pk>', DirectorDetail.as_view())
]