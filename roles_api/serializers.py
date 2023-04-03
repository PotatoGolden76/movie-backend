from rest_framework import serializers
from roles_api.models import RoleModel


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoleModel
        fields = '__all__'
