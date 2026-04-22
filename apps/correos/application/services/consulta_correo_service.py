import os
import base64
import pymysql
from django.conf import settings
from django.template.loader import render_to_string


class ConsultaCorreoService:
    @staticmethod
    def _obtener_conexion_pagina_web():
        return pymysql.connect(
            host=settings.DATABASES['pagina_web']['HOST'],
            user=settings.DATABASES['pagina_web']['USER'],
            password=settings.DATABASES['pagina_web']['PASSWORD'],
            database=settings.DATABASES['pagina_web']['NAME'],
            port=int(settings.DATABASES['pagina_web'].get('PORT') or 3308),
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

    @staticmethod
    def obtener_logo_base64():
        try:
            ruta_logo = os.path.join(
                settings.BASE_DIR,
                "apps",
                "correos",
                "infrastructure",
                "assets",
                "imagenCorporativaInacorp",
                "logoCorporativoInacorp.jpeg"
            )

            if not os.path.exists(ruta_logo):
                return ""

            with open(ruta_logo, "rb") as logo_file:
                logo_data = logo_file.read()
                logo_base64 = base64.b64encode(logo_data).decode("utf-8")

            return f"data:image/jpeg;base64,{logo_base64}"

        except Exception:
            return ""

    @staticmethod
    def obtener_orden_completa_prestashop(id_order: int):
        connection = None
        try:
            connection = ConsultaCorreoService._obtener_conexion_pagina_web()

            with connection.cursor() as cursor:
                cursor.execute("CALL SP_OBTENER_ORDEN_COMPLETA(%s)", (id_order,))
                resultados = cursor.fetchall()

            if not resultados:
                raise Exception(f"No se encontró la orden {id_order}")

            primera_fila = resultados[0]

            orden = {
                "id_order": primera_fila.get("id_order"),
                "id_cart": primera_fila.get("id_cart"),
                "referencia_orden": primera_fila.get("referencia_orden"),
                "total_pagado": primera_fila.get("total_pagado"),
                "metodo_pago": primera_fila.get("metodo_pago"),
                "estado_actual": primera_fila.get("estado_actual"),
                "fecha_pedido": primera_fila.get("fecha_pedido"),
                "id_customer": primera_fila.get("id_customer"),
                "firstname": primera_fila.get("firstname"),
                "lastname": primera_fila.get("lastname"),
                "correo_cliente": primera_fila.get("correo_cliente"),
                "address1": primera_fila.get("address1"),
                "address2": primera_fila.get("address2"),
                "city": primera_fila.get("city"),
                "postcode": primera_fila.get("postcode"),
                "phone": primera_fila.get("phone"),
                "phone_mobile": primera_fila.get("phone_mobile"),
            }

            productos = []
            for fila in resultados:
                if fila.get("nombre_producto"):
                    productos.append({
                        "referencia_producto": fila.get("referencia_producto"),
                        "nombre_producto": fila.get("nombre_producto"),
                        "cantidad": fila.get("cantidad"),
                        "precio_unitario": fila.get("precio_unitario"),
                        "total_linea": fila.get("total_linea"),
                    })

            return {
                "orden": orden,
                "productos": productos
            }

        except Exception as e:
            raise Exception(f"Error al obtener orden completa: {str(e)}")
        finally:
            if connection:
                connection.close()

    @staticmethod
    def construir_html_orden_prestashop(id_order: int):
        try:
            data = ConsultaCorreoService.obtener_orden_completa_prestashop(id_order)

            orden = data.get("orden")
            productos = data.get("productos", [])

            if not orden:
                raise Exception(f"No se encontró la orden {id_order}")

            if not productos:
                raise Exception(f"No se encontraron productos para la orden {id_order}")

            email = orden.get("correo_cliente", "")
            if not email:
                raise Exception("No se encontró el correo del cliente")

            logo_base64 = ConsultaCorreoService.obtener_logo_base64()
            productos_dict = [dict(p) for p in productos]

            total_items = sum(int(p.get("cantidad", 0) or 0) for p in productos_dict)
            total_pedido = float(orden.get("total_pagado", 0) or 0)

            cliente_nombre = f"{orden.get('firstname', '')} {orden.get('lastname', '')}".strip()

            contexto = {
                "logo_base64": logo_base64,
                "cliente_nombre": cliente_nombre,
                "numero_orden": orden.get("referencia_orden", ""),
                "fecha_creacion": orden.get("fecha_pedido", ""),
                "telefono": orden.get("phone_mobile") or orden.get("phone") or "",
                "email": email,
                "direccion_envio": " ".join(
                    filter(
                        None,
                        [
                            orden.get("address1", ""),
                            orden.get("address2", ""),
                            orden.get("city", ""),
                            orden.get("postcode", ""),
                        ],
                    )
                ),
                "total_items": total_items,
                "total_pedido": total_pedido,
                "productos": productos_dict,
                "orden": dict(orden),
            }

            html = render_to_string("correos/order_email_prestashop.html", contexto)

            return {
                "email": email,
                "html": html,
                "productos": productos_dict,
                "orden": dict(orden),
            }

        except Exception as e:
            raise Exception(f"Error en construir_html_orden_prestashop: {str(e)}")

    @staticmethod
    def enviar_correo_html(destinatario: str, asunto: str, html: str):
        raise Exception("Aquí debes conectar tu lógica real de envío con Graph")