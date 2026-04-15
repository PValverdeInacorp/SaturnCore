from decouple import config

from apps.correos.domain.entities.correo import Correo
from apps.correos.infrastructure.providers.graph_provider import GraphProvider
from apps.correos.application.services.render_correo_service import RenderCorreoService


DEFAULT_CC = [
    correo.strip()
    for correo in config("DEFAULT_CC", default="").split(",")
    if correo.strip()
]


class EnviarCorreoOrdenUseCase:
    @staticmethod
    def ejecutar(order_id: int):
        data = RenderCorreoService.construir_html_orden(order_id)
        orden = data["orden"]
        html = data["html"]

        email_destino = str(orden.get("EMAIL", "")).strip()
        if not email_destino:
            raise Exception("La orden no tiene correo electrónico destino")

        correo = Correo(
            destinatarios=[email_destino],
            asunto=f"Confirmación de compra {orden.get('NUMERO_DOCUMENTO', order_id)}",
            contenido_html=html,
            cc=DEFAULT_CC,
        )

        proveedor = GraphProvider()
        resultado = proveedor.enviar(correo)

        return {
            "ok": True,
            "mensaje": "Correo enviado correctamente",
            "order_id": order_id,
            "email_destino": email_destino,
            "status_code_graph": resultado["status_code_graph"],
        }