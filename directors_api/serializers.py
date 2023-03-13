from rest_framework import serializers
from directors_api.models import DirectorModel


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = DirectorModel
        fields = '__all__'
