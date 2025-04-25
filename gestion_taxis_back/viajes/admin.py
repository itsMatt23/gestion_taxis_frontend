from django.contrib import admin
from .models import Viaje

@admin.register(Viaje)
class ViajeAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'conductor', 'origen', 'destino', 'tarifa', 'estado', 'creado_en')
    list_filter = ('estado', 'creado_en')
    search_fields = ('cliente__nombre', 'conductor__nombre', 'origen', 'destino')