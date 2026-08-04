from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from .forms import CustomUserCreationForm

# VISTA DE REGISTRO
def register_view(request):
    if request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Inicia sesión tras el registro exitoso
            login(request, user)
            messages.success(request, f'¡Cuenta creada con éxito! Bienvenido, {user.username}.')
            return redirect('login')  # Hay que acomodar esto a la verdadera home
    else:
        form = CustomUserCreationForm()

    return render(request, 'users/register.html', {'form': form})


# VISTA DE LOGIN (Usamos la genérica de Django personalizada)
class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True  # Redirige si ya inició sesión


# VISTA DE LOGOUT (Usamos la genérica de Django)
class CustomLogoutView(LogoutView):
    next_page = 'login'  # Redirige al login tras cerrar sesión