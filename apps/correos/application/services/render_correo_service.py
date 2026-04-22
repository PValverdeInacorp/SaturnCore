import base64
import os
from pathlib import Path
from django.template.loader import render_to_string
from django.conf import settings

from apps.correos.application.services.obtener_orden_service import ObtenerOrdenService


class RenderCorreoService:
    """
    Servicio para renderizar HTML de correos y preparar datos para templates.
    Maneja la obtención de logos y renderización de plantillas HTML.
    """

    LOGO_FILENAME = "logo.png"

    @staticmethod
    def obtener_logo_base64():
        """
        Obtiene el logo de la empresa convertido a base64.
        
        Returns:
            String con el logo en formato base64 para usar en src de img.
            
        Raises:
            Exception: Si no encuentra el archivo del logo.
        """
        try:
            # Ruta del logo: apps/correos/infrastructure/assets/imagenPuntosInacorp/logo.png
            ruta_logo = os.path.join(
                settings.BASE_DIR,
                "apps",
                "correos",
                "infrastructure",
                "assets",
                "imagenPuntosInacorp",
                RenderCorreoService.LOGO_FILENAME
            )
            
            if not os.path.exists(ruta_logo):
                raise FileNotFoundError(f"Logo no encontrado en {ruta_logo}")
            
            with open(ruta_logo, "rb") as logo_file:
                logo_data = logo_file.read()
                logo_base64 = base64.b64encode(logo_data).decode("utf-8")
            
            return logo_base64
            
        except FileNotFoundError as e:
            raise Exception(f"Error al obtener logo: {str(e)}")
        except Exception as e:
            raise Exception(f"Error en obtener_logo_base64: {str(e)}")

    @staticmethod
    def construir_html_orden(order_id: int):
        """
        Construye el HTML del correo para una orden específica.
        
        Args:
            order_id: ID de la orden
            
        Returns:
            Diccionario con:
                - "orden": Datos de la orden
                - "html": HTML renderizado del correo
                - "productos": Lista de productos
                
        Raises:
            Exception: Si hay error al obtener datos o renderizar template.
        """
        try:
            # Obtener datos de la orden
            productos = ObtenerOrdenService.obtener_datos_orden(order_id)
            
            if not productos:
                raise Exception(f"No se encontró información para la orden {order_id}")
            
            # Usar el primer elemento como datos de la orden
            orden = productos[0]
            
            # Obtener logo en base64
            logo_base64 = RenderCorreoService.obtener_logo_base64()
            
            # Calcular total de items
            total_items = sum(int(item.get("CANTIDAD", 0)) for item in productos)
            
            # Preparar contexto para el template
            # Los campos corresponden a los que devuelve SP_OBTENER_ORDEN_COMPLETA
            contexto = {
                "logo_base64": logo_base64,
                "cliente_nombre": f"{orden.get('NOMBRES', '')} {orden.get('APELLIDOS', '')}".strip(),
                "numero_orden": orden.get("NUMERO_DOCUMENTO", ""),
                "fecha_creacion": orden.get("FECHA_CREACION", ""),
                "telefono": orden.get("TELEFONO", ""),
                "email": orden.get("EMAIL", ""),
                "direccion_envio": orden.get("DIRECCION_ENVIO", ""),
                "documento": orden.get("DOCUMENTO", ""),
                "total_puntos": orden.get("TOTAL_PUNTOS", 0),
                "total_items": total_items,
                "productos": productos,
                "orden": orden,
            }
            
            # Renderizar template
            html = render_to_string("correos/order_email.html", contexto)
            
            return {
                "orden": orden,
                "html": html,
                "productos": productos,
            }
            
        except Exception as e:
            raise Exception(f"Error en construir_html_orden: {str(e)}")
