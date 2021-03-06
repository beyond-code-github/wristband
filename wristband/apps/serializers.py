from rest_framework import serializers


class NestedAppSerializer(serializers.Serializer):
    name = serializers.CharField()
    version = serializers.CharField()
    stage = serializers.CharField()
    log_url = serializers.URLField(allow_null=True)


class AppSerializer(serializers.Serializer):
    name = serializers.CharField()
    stages = serializers.ListField(
        child=serializers.DictField(
            child=serializers.CharField(allow_null=True)
        )
    )