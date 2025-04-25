from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.routers import DefaultRouter
from .views import CustomUserViewSet
from .views import conductores_disponibles

from . import views

router = DefaultRouter()
router.register(r'usuarios', CustomUserViewSet)

urlpatterns = [
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Obtener token de acceso
    path('api/', include(router.urls)),
    path('api/buscar_usuario/', views.buscar_usuario, name='buscar_usuario'),
    path('api/conductores_disponibles/', conductores_disponibles, name='conductores_disponibles'),

]
