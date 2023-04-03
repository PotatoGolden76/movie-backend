from django.shortcuts import render

from rest_framework.response import Response
from rest_framework import status, generics
from roles_api.models import RoleModel
from roles_api.serializers import RoleSerializer
import math
from datetime import datetime


class Roles(generics.GenericAPIView):
    serializer_class = RoleSerializer
    queryset = RoleModel.objects.all()

    def get(self, request):
        page_num = int(request.GET.get("page", 1))
        limit_num = int(request.GET.get("limit", 10))
        start_num = (page_num - 1) * limit_num
        end_num = limit_num * page_num
        search_param = request.GET.get("search")
        roles = RoleModel.objects.all()
        total_roles = roles.count()
        if search_param:
            roles = roles.filter(title__icontains=search_param)
        serializer = self.serializer_class(
            roles[start_num:end_num], many=True)
        return Response({
            "status": "success",
            "total": total_roles,
            "page": page_num,
            "last_page": math.ceil(total_roles / limit_num),
            "roles": serializer.data
        })

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "role": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class RoleDetail(generics.GenericAPIView):
    queryset = RoleModel.objects.all()
    serializer_class = RoleSerializer

    def get_role(self, pk):
        try:
            return RoleModel.objects.get(pk=pk)
        except:
            return None

    def get(self, request, pk):
        role = self.get_role(pk=pk)
        if role == None:
            return Response({"status": "fail", "message": f"role with Id: {pk} not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(role)
        return Response({"status": "success", "role": serializer.data})

    def patch(self, request, pk):
        role = self.get_role(pk)
        if role == None:
            return Response({"status": "fail", "message": f"role with Id: {pk} not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(
            role, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "role": serializer.data})
        return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        role = self.get_role(pk)
        if role == None:
            return Response({"status": "fail", "message": f"role with Id: {pk} not found"}, status=status.HTTP_404_NOT_FOUND)

        role.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
