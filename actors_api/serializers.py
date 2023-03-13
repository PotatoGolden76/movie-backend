from rest_framework import serializers
from actors_api.models import ActorModel


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActorModel
        fields = '__all__'
