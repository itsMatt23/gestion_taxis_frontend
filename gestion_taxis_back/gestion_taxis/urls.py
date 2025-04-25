from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    #path('admin/', admin.site.urls),
    #Login con seguirdad JWT
    path('usuarios/', include('usuarios.urls')),
    path('api/', include('viajes.urls')),
]
