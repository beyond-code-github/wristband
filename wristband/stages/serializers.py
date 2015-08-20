from rest_framework import serializers

class StageSerializer(serializers.Serializer):
    name = serializers.CharField()

