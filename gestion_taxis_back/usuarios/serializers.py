from rest_framework import serializers
from .models import CustomUser


class ConductorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id',
            'nombre',
            'apellido',
            'cedula',
            'email',
            'telefono',
            'marca_vehiculo',
            'placa',
            'estado',
        ]


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id', 'email', 'cedula', 'nombre', 'apellido', 
            'telefono', 'rol', 'marca_vehiculo', 'placa', 'estado', 'password',
        ]
        extra_kwargs = {
            'email': {'required': True},
            'cedula': {'required': True},
            'password': {'write_only': True, 'required': False},  # Contraseña opcional
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        if not password:
            raise serializers.ValidationError({"password": "La contraseña es requerida al crear un usuario."})
        
        user = CustomUser.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        # La contraseña es opcional al actualizar
        password = validated_data.pop('password', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)  # Si se proporciona, actualiza la contraseña
        else:
            # No cambiar la contraseña si no se proporciona
            instance.password = instance.password

        instance.save()
        return instance
