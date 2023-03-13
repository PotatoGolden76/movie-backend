from directors_api.views import Directors, DirectorDetail, DirectorFilter
from django.urls import path

urlpatterns = [
    path('', Directors.as_view()),
    path('<str:pk>', DirectorDetail.as_view()),
    path('filter/<str:val>', DirectorFilter.as_view())
]