from django.db import models

class Viaje(models.Model):
    cliente = models.ForeignKey(
        'usuarios.CustomUser',
        on_delete=models.CASCADE,
        related_name='viajes_cliente',
        limit_choices_to={'rol': 'Cliente'}
    )
    conductor = models.ForeignKey(
        'usuarios.CustomUser',
        on_delete=models.CASCADE,
        related_name='viajes_conductor',
        limit_choices_to={'rol': 'Conductor'},
        blank=True,
        null=True
    )
    origen = models.CharField(max_length=255)
    destino = models.CharField(max_length=255)
    tarifa = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(
        max_length=20,
        choices=[
            ('pendiente', 'Pendiente'),
            ('en_progreso', 'En Progreso'),
            ('completado', 'Completado')
        ],
        default='pendiente'
    )
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Viaje {self.id} - Cliente: {self.cliente.email}"
