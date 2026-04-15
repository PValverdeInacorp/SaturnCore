from django.db import models


class HistorialCorreo(models.Model):
    order_id = models.IntegerField()
    destinatario = models.EmailField()
    asunto = models.CharField(max_length=255)
    estado = models.CharField(max_length=50, default="ENVIADO")
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "historial_correos"