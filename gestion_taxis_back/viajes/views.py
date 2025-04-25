from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from .models import Viaje
from .serializers import ViajeSerializer
from usuarios.models import CustomUser

class ViajeViewSet(ModelViewSet):
    queryset = Viaje.objects.all()
    serializer_class = ViajeSerializer

    @action(detail=True, methods=['POST'])
    def completar(self, request, pk=None):
        """
        Cambia el estado de un viaje a 'completado' y libera al conductor.
        """
        viaje = self.get_object()
        viaje.refresh_from_db()  # Recarga los datos más recientes de la base de datos

        if viaje.estado != 'en_progreso':
            return Response({"error": "El viaje no está en progreso."}, status=status.HTTP_400_BAD_REQUEST)

        viaje.estado = 'completado'
        viaje.conductor.estado = 'Libre'
        viaje.conductor.save()
        viaje.save()
        return Response({"mensaje": "El viaje se ha completado exitosamente."})

    @action(detail=True, methods=['POST'])
    def finalizar(self, request, pk=None):
        """
        Finaliza un viaje en progreso.
        """
        viaje = self.get_object()
        if viaje.estado != 'en_progreso':
            return Response({"error": "El viaje no se puede finalizar porque no está en progreso."},
                            status=status.HTTP_400_BAD_REQUEST)

        viaje.estado = 'completado'
        viaje.conductor.estado = 'Libre'
        viaje.conductor.save()
        viaje.save()
        return Response({"mensaje": f"El viaje {viaje.id} se ha finalizado correctamente."})

    @action(detail=True, methods=['POST'])
    def cancelar(self, request, pk=None):
        """
        Cancela un viaje y libera al conductor si está asignado.
        """
        viaje = self.get_object()
        if viaje.estado == 'completado':
            return Response({"error": "No se puede cancelar un viaje ya completado."}, status=status.HTTP_400_BAD_REQUEST)

        viaje.estado = 'cancelado'
        if viaje.conductor:
            viaje.conductor.estado = 'Libre'
            viaje.conductor.save()
        viaje.save()
        return Response({"mensaje": f"El viaje {viaje.id} se ha cancelado correctamente."})

    @action(detail=True, methods=['POST'])
    def asignar_conductor(self, request, pk=None):
        """
        Asigna un conductor disponible a un viaje pendiente.
        """
        viaje = self.get_object()
        if viaje.estado != 'pendiente':
            return Response({"error": "Solo se pueden asignar conductores a viajes pendientes."},
                            status=status.HTTP_400_BAD_REQUEST)

        conductor = CustomUser.objects.filter(rol='Conductor', estado='Libre').first()
        if not conductor:
            return Response({"error": "No hay conductores disponibles."}, status=status.HTTP_400_BAD_REQUEST)

        viaje.conductor = conductor
        viaje.estado = 'en_progreso'
        conductor.estado = 'Ocupado'
        conductor.save()
        viaje.save()
        return Response({"mensaje": f"Conductor asignado al viaje {viaje.id}."})

    def list(self, request, *args, **kwargs):
        """
        Listar todos los viajes con posibilidad de filtrar por estado, cliente o conductor.
        """
        estado = request.query_params.get('estado')
        cliente_id = request.query_params.get('cliente')
        conductor_id = request.query_params.get('conductor')

        queryset = Viaje.objects.all()

        if estado:
            queryset = queryset.filter(estado=estado)
        if cliente_id:
            queryset = queryset.filter(cliente_id=cliente_id)
        if conductor_id:
            queryset = queryset.filter(conductor_id=conductor_id)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    def historial_cliente(self, request):
        """
        Lista todos los viajes de un cliente específico.
        """
        cliente_id = request.query_params.get('cliente')
        if not cliente_id:
            return Response({"error": "El parámetro 'cliente' es requerido."}, status=status.HTTP_400_BAD_REQUEST)

        queryset = self.queryset.filter(cliente_id=cliente_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    def historial_conductor(self, request):
        """
        Lista todos los viajes realizados por un conductor específico.
        """
        conductor_id = request.query_params.get('conductor')
        if not conductor_id:
            return Response({"error": "El parámetro 'conductor' es requerido."}, status=status.HTTP_400_BAD_REQUEST)

        queryset = self.queryset.filter(conductor_id=conductor_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def get_queryset(self):
        # Asegúrate de siempre obtener los datos más actualizados
        return Viaje.objects.all()
    
    @action(detail=False, methods=['GET'], url_path='asignado/(?P<conductor_id>[^/.]+)')
    def viaje_asignado(self, request, conductor_id=None):
        """
        Devuelve el viaje en progreso asignado a un conductor específico.
        Si no hay un viaje, devuelve un mensaje claro.
        """
        try:
            # Filtrar viaje en progreso para el conductor
            viaje = Viaje.objects.filter(conductor_id=conductor_id, estado='en_progreso').first()
            
            if not viaje:
                # Si no hay viaje en progreso, retorna un mensaje claro
                return Response(
                    {"mensaje": "Por el momento no dispone de viajes en progreso."}, 
                    status=status.HTTP_200_OK
                )
            
            # Si existe un viaje, lo serializa y devuelve
            serializer = self.get_serializer(viaje)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            # Manejar errores inesperados
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
