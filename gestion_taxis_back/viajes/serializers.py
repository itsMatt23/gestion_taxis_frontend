from rest_framework import serializers
from .models import Viaje
from usuarios.models import CustomUser

class ConductorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'nombre', 'cedula','apellido','email', 'telefono']  # Incluye los campos que deseas mostrar del conductor
        
class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'nombre', 'apellido', 'cedula', 'email', 'telefono']  # Ajusta los campos según lo necesario


class ViajeSerializer(serializers.ModelSerializer):
    cliente_id = serializers.IntegerField(write_only=True, required=True)  # Campo para recibir el cliente_id

    cliente = ClienteSerializer(read_only=True)  # Anida el serializador del cliente

    conductor = ConductorSerializer(read_only=True)  # Anida el serializador del conductor

    class Meta:
        model = Viaje
        fields = '__all__'
        read_only_fields = ['estado', 'conductor']

    def create(self, validated_data):
               # Extraer cliente_id de los datos validados
        cliente_id = validated_data.get('cliente_id')
        try:
            # Obtener el objeto cliente usando cliente_id
            cliente = CustomUser.objects.get(id=cliente_id, rol='Cliente')
            cliente.refresh_from_db()
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError({"cliente_id": "Cliente no encontrado o no válido."})

        viaje_en_proceso = Viaje.objects.filter(cliente=cliente, estado__in=['pendiente', 'en_progreso']).exists()
    
        if viaje_en_proceso:
            raise serializers.ValidationError(
                {"error": "Ya tienes un viaje en proceso. No puedes solicitar otro hasta que se complete el actual."}
            )
    
        # Asignar un conductor disponible

        conductor = CustomUser.objects.filter(rol='Conductor', estado='Libre').first()
        if not conductor:
            raise serializers.ValidationError({"error": "No hay conductores disponibles."})
    
        # Actualizar conductor y estado
        validated_data['conductor'] = conductor
        validated_data['estado'] = 'en_progreso'
        conductor.estado = 'Ocupado'
        conductor.save()
    
        return super().create(validated_data)