from rest_framework import serializers
from .models import Emisor, CalificacionTributaria, ArchivoCargado

class EmisorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emisor
        fields = '__all__'


class CalificacionTributariaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalificacionTributaria
        fields = '__all__'


class ArchivoCargadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArchivoCargado
        fields = '__all__'
