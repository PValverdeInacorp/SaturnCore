from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from apps.correos.api.serializers import EnviarCorreoRequestSerializer
from apps.correos.application.use_cases.enviar_correo_orden import EnviarCorreoOrdenUseCase
from apps.correos.application.use_cases.generar_pdf_orden import GenerarPdfOrdenUseCase


class EnviarCorreoView(APIView):

    @swagger_auto_schema(
        operation_summary="Enviar correo por orden",
        operation_description="Envía un correo basado en el ID de la orden",
        request_body=EnviarCorreoRequestSerializer,
        responses={
            200: openapi.Response(
                description="Correo enviado correctamente"
            ),
            400: "Error en datos",
            500: "Error interno"
        },
        tags=["Correos"]
    )

    def post(self, request):
        serializer = EnviarCorreoRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            resultado = EnviarCorreoOrdenUseCase.ejecutar(
                serializer.validated_data["order_id"]
            )
            return Response(resultado, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"ok": False, "mensaje": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class GenerarPdfView(APIView):
    def get(self, request, order_id):
        try:
            pdf_bytes, nombre = GenerarPdfOrdenUseCase.ejecutar(order_id)
            response = HttpResponse(pdf_bytes, content_type="application/pdf")
            response["Content-Disposition"] = f'inline; filename="{nombre}.pdf"'
            return response
        except Exception as e:
            return Response(
                {"ok": False, "mensaje": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )