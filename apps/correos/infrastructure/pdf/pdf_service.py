from io import BytesIO
from django.template.loader import render_to_string
from xhtml2pdf import pisa

from apps.correos.application.services.obtener_orden_service import ObtenerOrdenService
from apps.correos.application.services.render_correo_service import RenderCorreoService


class PdfService:
    @classmethod
    def generar_pdf_por_order_id(cls, order_id: int):
        productos = ObtenerOrdenService.obtener_datos_orden(order_id)

        if not productos:
            raise Exception(f"No se encontró información para la orden {order_id}")

        orden = productos[0]
        total_items = sum(int(item.get("CANTIDAD", 0)) for item in productos)
        logo_base64 = RenderCorreoService.obtener_logo_base64()

        html_pdf = render_to_string(
            "correos/order_pdf.html",
            {
                "orden": orden,
                "productos": productos,
                "logo_base64": logo_base64,
                "total_items": total_items,
            },
        )

        resultado = BytesIO()
        pdf = pisa.CreatePDF(src=html_pdf, dest=resultado)

        if pdf.err:
            raise Exception("No se pudo generar el PDF")

        return resultado.getvalue(), orden