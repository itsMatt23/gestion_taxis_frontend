# auditoria/models.py

from django.db import models

class AuditoriaViajes(models.Model):
    viaje = models.ForeignKey('viajes.Viaje', on_delete=models.CASCADE, related_name='auditorias')
    realizado_por = models.ForeignKey('usuarios.CustomUser', on_delete=models.SET_NULL, null=True, blank=True)
    tipo_cambio = models.CharField(max_length=50)
    valor_anterior = models.TextField(null=True, blank=True)
    valor_nuevo = models.TextField(null=True, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Auditoría de Viaje {self.viaje.id} - Cambio: {self.tipo_cambio}"
