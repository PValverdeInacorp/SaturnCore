from rest_framework import serializers


class EnviarCorreoRequestSerializer(serializers.Serializer):
    order_id = serializers.IntegerField(required=True)