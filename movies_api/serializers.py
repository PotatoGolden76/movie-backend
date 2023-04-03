from rest_framework import serializers
from movies_api.models import MovieModel


class MovieSerializer(serializers.ModelSerializer):
    actor_count = serializers.IntegerField(default=0)
    class Meta:
        model = MovieModel
        fields = '__all__'
