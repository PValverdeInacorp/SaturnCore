from django.db import connections


class MysqlOrdenRepository:
    """
    Repositorio para acceder a datos de órdenes en MySQL
    usando el procedimiento almacenado SP_OBTENER_ORDEN_COMPLETA.
    """

    @staticmethod
    def obtener_orden_completa(order_id: int):
        """
        Obtiene una orden completa desde el SP:
        - Primer resultset: cabecera
        - Segundo resultset: detalle

        Args:
            order_id: ID de la orden

        Returns:
            Diccionario con los datos de la orden y sus productos

        Raises:
            Exception: Si no encuentra la orden o hay error de BD
        """
        try:
            conn = connections["puntos"]  # Cambiar si tu conexión tiene otro alias
            cursor = conn.cursor()

            cursor.callproc("SP_OBTENER_ORDEN_COMPLETA", [order_id])

            # Primer resultset: cabecera
            orden = None
            if cursor.description:
                columnas_orden = [col[0] for col in cursor.description]
                fila_orden = cursor.fetchone()

                if fila_orden:
                    orden = dict(zip(columnas_orden, fila_orden))

            # Segundo resultset: detalle
            productos = []
            if cursor.nextset():
                if cursor.description:
                    columnas_productos = [col[0] for col in cursor.description]
                    filas_productos = cursor.fetchall()
                    productos = [
                        dict(zip(columnas_productos, fila))
                        for fila in filas_productos
                    ]

            cursor.close()

            if not orden:
                raise Exception(f"Orden {order_id} no encontrada")

            return {
                "orden": orden,
                "productos": productos,
            }

        except Exception as e:
            raise Exception(f"Error al obtener orden completa: {str(e)}")