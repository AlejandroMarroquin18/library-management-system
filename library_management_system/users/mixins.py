from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied


class AdminRequiredMixin(UserPassesTestMixin):
    """
    Mixin para Class-Based Views.
    Permite el acceso únicamente si el rol del usuario es 'ADMIN' o es superusuario.
    Rechaza con HTTP 403 (PermissionDenied) a cualquier CUSTOMER u otro rol.
    """
    def test_func(self):
        user = self.request.user
        
        # 1. Validar autenticación
        if not user.is_authenticated:
            return False

        # 2. Si es Superusuario de Django, permitir siempre
        if user.is_superuser:
            return True

        # 3. Validar de forma estricta el campo 'role' de tu CustomUser
        # Asegúrate de comparar contra la constante/string exacto que guardas en la DB ('ADMIN')
        user_role = getattr(user, 'role', None)
        
        return user_role == 'ADMIN'

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            raise PermissionDenied("No tienes permisos de administrador para acceder a este panel.")
        return super().handle_no_permission()