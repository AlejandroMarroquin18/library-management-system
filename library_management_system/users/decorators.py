from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect

def admin_required(view_func):
    """
    Decorador que restringe el acceso solo a usuarios con rol ADMIN o superusuarios.
    """
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        
        # Usamos el método helper que definimos en el modelo User
        if request.user.is_admin():
            return view_func(request, *args, **kwargs)
        
        # Si es un usuario normal (CUSTOMER), le denegamos el acceso (403 Forbidden)
        raise PermissionDenied
        
    return _wrapped_view