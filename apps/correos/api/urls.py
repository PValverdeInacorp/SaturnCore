from django.urls import path
from apps.correos.api.views import EnviarCorreoView, GenerarPdfView

urlpatterns = [
    path("send/", EnviarCorreoView.as_view(), name="enviar_correo"),
    path("pdf/<int:order_id>/", GenerarPdfView.as_view(), name="generar_pdf"),
]