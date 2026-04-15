from apps.correos.infrastructure.pdf.pdf_service import PdfService


class GenerarPdfOrdenUseCase:
    @staticmethod
    def ejecutar(order_id: int):
        pdf_bytes, orden = PdfService.generar_pdf_por_order_id(order_id)
        nombre = orden.get("NUMERO_DOCUMENTO", f"orden_{order_id}")
        return pdf_bytes, nombre