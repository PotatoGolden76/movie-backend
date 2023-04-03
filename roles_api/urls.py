from django.urls import path
from roles_api.views import Roles, RoleDetail

urlpatterns = [
    path('', Roles.as_view()),
    path('<str:pk>', RoleDetail.as_view())
]