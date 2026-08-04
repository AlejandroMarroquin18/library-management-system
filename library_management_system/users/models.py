from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

# Modelo de usuario personalizado que hereda de AbstractUser. 
# Agrega un campo de rol con opciones de administrador y cliente, y un campo de fecha de creación. 
# También incluye métodos para verificar si el usuario es administrador o cliente.
class User(AbstractUser):

    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('CUSTOMER', 'Customer'),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='CUSTOMER')
    created_at = models.DateTimeField(auto_now_add=True)

    def is_admin(self):
        return self.role == 'ADMIN' or self.is_superuser

    def is_customer(self):
        return self.role == 'CUSTOMER'