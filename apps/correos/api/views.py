from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from apps.correos.api.serializers import (
    EnviarCorreoRequestSerializer,
    EnviarCorreoConsultaSerializer,
    EnviarCorreoOrdenPrestashopSerializer,
)
from apps.correos.application.use_cases.enviar_correo_orden import EnviarCorreoOrdenUseCase
from apps.correos.application.use_cases.generar_pdf_orden import GenerarPdfOrdenUseCase
from apps.correos.application.use_cases.enviar_correo_consulta_prestahop import EnviarCorreoConsultaUseCase
from apps.correos.application.use_cases.enviar_correo_orden_prestashop import EnviarCorreoOrdenPrestashopUseCase


class EnviarCorreoView(APIView):
    @swagger_auto_schema(
        operation_summary="Enviar correo por orden",
        operation_description="Envía un correo basado en el ID de la orden",
        request_body=EnviarCorreoRequestSerializer,
        responses={
            200: openapi.Response(description="Correo enviado correctamente"),
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
    @swagger_auto_schema(
        operation_summary="Generar PDF de orden",
        operation_description="Genera un PDF basado en el ID de la orden",
        responses={
            200: openapi.Response(description="PDF generado correctamente"),
            404: "Orden no encontrada",
            500: "Error interno"
        },
        tags=["Correos"]
    )
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


class EnviarCorreoConsultaView(APIView):
    @swagger_auto_schema(
        operation_summary="Enviar correo de consulta",
        operation_description="Envía un correo con datos de consulta obtenidos de procedimientos almacenados",
        request_body=EnviarCorreoConsultaSerializer,
        responses={
            200: openapi.Response(description="Correo enviado correctamente"),
            400: "Error en datos",
            500: "Error interno"
        },
        tags=["Correos"]
    )
    def post(self, request):
        try:
            resultado = EnviarCorreoConsultaUseCase.ejecutar()
            return Response(resultado, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"ok": False, "mensaje": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class EnviarCorreoOrdenPrestashopView(APIView):
    @swagger_auto_schema(
        operation_summary="Enviar correo de pedido PrestaShop",
        operation_description="Envía un correo de confirmación usando el id_order generado en PrestaShop",
        request_body=EnviarCorreoOrdenPrestashopSerializer,
        responses={
            200: openapi.Response(description="Correo enviado correctamente"),
            400: "Error en datos",
            500: "Error interno"
        },
        tags=["Correos"]
    )
    def post(self, request):
        serializer = EnviarCorreoOrdenPrestashopSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            resultado = EnviarCorreoOrdenPrestashopUseCase.ejecutar(
                serializer.validated_data["id_order"]
            )
            return Response(resultado, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"ok": False, "mensaje": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )