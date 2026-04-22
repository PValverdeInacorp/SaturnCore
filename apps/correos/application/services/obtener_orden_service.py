import pymysql
from django.conf import settings


class ObtenerOrdenService:
    """
    Servicio para obtener los datos de una orden desde la base de datos MySQL.
    Usa el procedimiento almacenado SP_OBTENER_ORDEN_COMPLETA.
    """

    @staticmethod
    def _obtener_conexion_puntos():
        """
        Obtiene una conexión directa a la BD puntos.
        """
        return pymysql.connect(
            host=settings.DATABASES['puntos']['HOST'],
            user=settings.DATABASES['puntos']['USER'],
            password=settings.DATABASES['puntos']['PASSWORD'],
            database=settings.DATABASES['puntos']['NAME'],
            port=int(settings.DATABASES['puntos']['PORT']),
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

    @staticmethod
    def obtener_datos_orden(order_id: int):
        """
        Obtiene los datos de una orden específica usando el procedimiento almacenado.
        
        Args:
            order_id: ID de la orden a obtener
            
        Returns:
            Lista de diccionarios con los datos de la orden y sus productos.
            
        Raises:
            Exception: Si hay error en la ejecución del procedimiento
        """
        connection = None
        try:
            connection = ObtenerOrdenService._obtener_conexion_puntos()
            
            with connection.cursor() as cursor:
                # Ejecutar stored procedure
                cursor.execute(f"CALL SP_OBTENER_ORDEN_COMPLETA({order_id})")
                resultados = cursor.fetchall()
            
            if not resultados:
                raise Exception(f"No se encontró información para la orden {order_id}")
            
            return resultados
            
        except Exception as e:
            raise Exception(f"Error al obtener datos de la orden: {str(e)}")
        finally:
            if connection:
                connection.close()
