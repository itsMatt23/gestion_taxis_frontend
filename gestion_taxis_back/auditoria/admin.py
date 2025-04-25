from django.contrib import admin
from .models import AuditoriaViajes

@admin.register(AuditoriaViajes)
class AuditoriaViajesAdmin(admin.ModelAdmin):
    list_display = ('id', 'viaje', 'realizado_por', 'tipo_cambio', 'creado_en')
    list_filter = ('tipo_cambio', 'creado_en')
    search_fields = ('viaje__id', 'realizado_por__nombre', 'tipo_cambio')