from django.urls import path
from apps.correos.api.views import EnviarCorreoView, GenerarPdfView, EnviarCorreoConsultaView, EnviarCorreoOrdenPrestashopView

urlpatterns = [
    path("send/", EnviarCorreoView.as_view(), name="enviar_correo"),# url para enviar el correo para puntos inacorp sa
    path("pdf/<int:order_id>/", GenerarPdfView.as_view(), name="generar_pdf"), # url para generar el pdf de la orden
    path("consulta/", EnviarCorreoConsultaView.as_view(), name="enviar_correo_consulta"), #  para el envio de la orden de la pagina wed
    path("prestashop/", EnviarCorreoOrdenPrestashopView.as_view(), name="enviar_correo_orden_prestashop"),
]