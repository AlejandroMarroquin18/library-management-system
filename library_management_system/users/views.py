from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
import logging
from .forms import CustomUserCreationForm

logger = logging.getLogger(__name__)


# VISTA DE REGISTRO
def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Inicia sesión automáticamente tras registrarse
            login(request, user)
            messages.success(request, f'¡Cuenta creada con éxito! Bienvenido, {user.username}.')
            logger.info('user_registered user_id=%s method=password', user.pk)
            return redirect('home')  # Redirige directamente al catálogo principal
        else:
            messages.error(request, "Por favor corrige los errores del formulario.")
    else:
        form = CustomUserCreationForm()

    return render(request, 'users/register.html', {'form': form})


# VISTA DE LOGIN
class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        messages.success(self.request, f"¡Hola de nuevo, {form.get_user().username}!")
        logger.info('user_login_succeeded user_id=%s method=password', form.get_user().pk)
        return super().form_valid(form)

    def form_invalid(self, form):
        logger.warning('user_login_failed username=%s', form.data.get('username', '<empty>'))
        return super().form_invalid(form)


# VISTA DE LOGOUT
class CustomLogoutView(LogoutView):
    next_page = 'login'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, "Has cerrado sesión correctamente.")
        return super().dispatch(request, *args, **kwargs)