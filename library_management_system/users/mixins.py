from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied


class AdminRequiredMixin(UserPassesTestMixin):
    """
    Mixin para Class-Based Views.
    Permite el acceso únicamente a usuarios con rol ADMIN o superusuarios.
    Rechaza con un HTTP 403 (PermissionDenied) si es un CUSTOMER.
    """
    def test_func(self):
        user = self.request.user
        if not user.is_authenticated:
            return False
        
        # Asumiendo que tu CustomUser tiene un atributo 'role' o 'is_staff' / 'is_superuser'
        is_admin_role = getattr(user, 'role', None) == 'ADMIN' or getattr(user, 'is_admin', False)
        return is_admin_role or user.is_staff or user.is_superuser

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            raise PermissionDenied("No tienes permisos de administrador para acceder a esta sección.")
        return super().handle_no_permission()