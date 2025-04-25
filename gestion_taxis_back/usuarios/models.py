from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("El correo electrónico es obligatorio")
        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', True)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("El superusuario debe tener is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("El superusuario debe tener is_superuser=True.")

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLES = [
        ('Cliente', 'Cliente'),
        ('Admin', 'Admin'),
        ('Conductor', 'Conductor'),
    ]
    
    ESTADO_CHOICES_CONDUCTOR = [
        ('Libre', 'Libre'),
        ('Ocupado', 'Ocupado'),
    ]

    email = models.EmailField(unique=True)
    cedula = models.CharField(max_length=10, unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    rol = models.CharField(max_length=10, choices=ROLES, default='Admin')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Campos específicos para conductores
    marca_vehiculo = models.CharField(max_length=100, blank=True, null=True)
    placa = models.CharField(max_length=10, blank=True, null=True)
    estado = models.CharField(
        max_length=10,
        choices=[('Libre', 'Libre'), ('Ocupado', 'Ocupado')],
        blank=True,
        null=True,
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['cedula', 'nombre', 'apellido', 'telefono']

    def save(self, *args, **kwargs):
        if self.rol != 'Conductor':
            self.marca_vehiculo = None
            self.placa = None
            self.estado = None
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email
