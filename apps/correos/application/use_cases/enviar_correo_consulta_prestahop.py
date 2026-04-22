from decouple import config

from apps.correos.application.services.consulta_correo_service import ConsultaCorreoService
from apps.correos.domain.entities.correo import Correo
from apps.correos.infrastructure.providers.graph_provider import GraphProvider


DEFAULT_CC = [
    correo.strip()
    for correo in config("DEFAULT_CC", default="").split(",")
    if correo.strip()
]

DEFAULT_BCC = [
    correo.strip()
    for correo in config("DEFAULT_BCC", default="").split(",")
    if correo.strip()
]


class EnviarCorreoConsultaUseCase:
    @staticmethod
    def ejecutar():
        try:
            data = ConsultaCorreoService.construir_html_consulta()

            email_destino = data["email"]
            html = data["html"]
            productos = data["productos"]

            if not email_destino:
                raise Exception("No se encontró correo electrónico destino")

            correo = Correo(
                destinatarios=[email_destino],
                asunto="Consulta - Confirmación de productos disponibles",
                contenido_html=html,
                cc=DEFAULT_CC,
                bcc=DEFAULT_BCC,
            )

            proveedor = GraphProvider()
            resultado = proveedor.enviar(correo)

            return {
                "ok": True,
                "mensaje": "Correo enviado correctamente",
                "email_destino": email_destino,
                "cantidad_productos": len(productos),
                "status_code_graph": resultado.get("status_code_graph"),
            }

        except Exception as e:
            raise Exception(f"Error en EnviarCorreoConsultaUseCase: {str(e)}")