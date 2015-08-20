from rest_framework import serializers


class AppSerializer(serializers.Serializer):
    name = serializers.CharField()
    version = serializers.CharField()
    stage = serializers.CharField()
