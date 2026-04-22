from rest_framework import serializers


class EnviarCorreoRequestSerializer(serializers.Serializer):
    order_id = serializers.IntegerField(required=True)


class EnviarCorreoConsultaSerializer(serializers.Serializer):
    """
    Serializer para envío de correos de consulta.
    No requiere parámetros (obtiene datos directamente de los SP).
    """
    pass



class EnviarCorreoOrdenPrestashopSerializer(serializers.Serializer):
    id_order = serializers.IntegerField(required=True)