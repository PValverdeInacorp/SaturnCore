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


class EnviarCorreoOrdenPrestashopUseCase:
    @staticmethod
    def ejecutar(id_order: int):
        try:
            data = ConsultaCorreoService.construir_html_orden_prestashop(id_order)

            email_destino = data["email"]
            html = data["html"]
            productos = data["productos"]
            orden = data["orden"]

            if not email_destino:
                raise Exception("No se encontró correo electrónico destino")

            correo = Correo(
                destinatarios=[email_destino],
                asunto=f"Confirmación de pedido #{orden.get('referencia_orden', '')}",
                contenido_html=html,
                cc=DEFAULT_CC,
                bcc=DEFAULT_BCC,
            )

            proveedor = GraphProvider()
            resultado = proveedor.enviar(correo)

            return {
                "ok": True,
                "mensaje": "Correo de pedido enviado correctamente",
                "email_destino": email_destino,
                "id_order": id_order,
                "referencia": orden.get("referencia_orden", ""),
                "cantidad_productos": len(productos),
                "status_code_graph": resultado.get("status_code_graph"),
            }

        except Exception as e:
            raise Exception(f"Error en EnviarCorreoOrdenPrestashopUseCase: {str(e)}")