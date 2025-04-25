from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from .models import CustomUser
from .serializers import CustomUserSerializer, ConductorSerializer
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.permissions import AllowAny

class CustomUserViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        # Obtener los datos del request
        data = request.data

        # Validaciones personalizadas
        errors = {}

        # Validar si el email ya está registrado
        if CustomUser.objects.filter(email=data.get('email')).exists():
            errors['email'] = ["El correo electrónico ya está registrado."]

        # Validar si la cédula ya está registrada
        if CustomUser.objects.filter(cedula=data.get('cedula')).exists():
            errors['cedula'] = ["La cédula ya está registrada."]

        # Validar si el teléfono ya está registrado
        if CustomUser.objects.filter(telefono=data.get('telefono')).exists():
            errors['telefono'] = ["El número de teléfono ya está registrado."]

        # Si hay errores, devolver la respuesta con los mensajes de error
        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        # Si las validaciones pasan, proceder con la creación del usuario
        return super().create(request, *args, **kwargs)
    
#######################################
@api_view(['GET'])
def buscar_usuario(request):
    email = request.GET.get('email', '')
    if email:
        try:
            user = CustomUser.objects.get(email=email)
            serializer = CustomUserSerializer(user)
            return Response(serializer.data)
        except CustomUser.DoesNotExist:
            return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({"error": "El parámetro 'email' es requerido"}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
def conductores_disponibles(request):
    conductores = CustomUser.objects.filter(rol='Conductor', estado='Libre')
    serializer = ConductorSerializer(conductores, many=True)
    return Response(serializer.data)