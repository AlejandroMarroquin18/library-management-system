from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from .forms import CustomUserCreationForm


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
        return super().form_valid(form)


# VISTA DE LOGOUT
class CustomLogoutView(LogoutView):
    next_page = 'login'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, "Has cerrado sesión correctamente.")
        return super().dispatch(request, *args, **kwargs)