from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Clase CustomUserAdmin que hereda de UserAdmin para personalizar la administración del modelo de usuario personalizado. 
# Se configuran los campos que se mostrarán en la lista de usuarios, 
# los filtros disponibles y los campos que se mostrarán en los formularios de edición y 
# creación de usuarios. 
# Finalmente, se registra el modelo User con la clase CustomUserAdmin en el panel de administración.
class CustomUserAdmin(UserAdmin):
    # Configuración de los campos que se mostrarán en la lista de usuarios en el panel de administración
    list_display = ('username', 'email', 'role', 'is_staff', 'created_at')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active')

    fieldsets = UserAdmin.fieldsets + (
        ('Información de Rol', {'fields': ('role',)}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información de Rol', {'fields': ('role',)}),
    )

# Register your models here.
admin.site.register(User, CustomUserAdmin)