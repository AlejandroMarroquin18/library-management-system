from datetime import timedelta
from django.db import transaction
from django.views.generic import DetailView, TemplateView, ListView, CreateView, UpdateView, DeleteView, View
from django.utils import timezone
from django.contrib.auth import get_user_model
from users.mixins import AdminRequiredMixin
from catalog.models import Autor, Categoria, Editorial, Libro
from sales.models import Compra
from loans.models import Loan
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404

User = get_user_model()

class DashboardHomeView(AdminRequiredMixin, TemplateView):
    """
    Vista principal del Panel de Control.
    Calcula dinámicamente las métricas clave sin tocar el /admin de Django.
    """
    template_name = 'dashboard/dashboard_home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()

        # Métricas principales
        context['total_libros'] = Libro.objects.count()
        context['total_usuarios'] = User.objects.count()
        context['total_compras'] = Compra.objects.count()
        
        # Consultas de Préstamos corregidas con los campos reales
        # Un préstamo está activo si no tiene registrada una fecha de devolución
        context['prestamos_activos'] = Loan.objects.filter(returned_date__isnull=True).count()
        
        # Un préstamo está vencido si no se ha devuelto y la fecha límite (due_date) ya pasó
        context['prestamos_vencidos'] = Loan.objects.filter(
            returned_date__isnull=True, 
            due_date__lt=now
        ).count()

        return context

class AutorListView(AdminRequiredMixin, ListView):
    model = Autor
    template_name = 'dashboard/autores/autor_list.html'
    context_object_name = 'autores'
    paginate_by = 10


class AutorCreateView(AdminRequiredMixin, CreateView):
    model = Autor
    fields = ['nombre', 'apellido', 'biografia', 'fecha_nacimiento', 'pais']
    template_name = 'dashboard/autores/autor_form.html'
    success_url = reverse_lazy('dashboard:autor_list')

    def form_valid(self, form):
        messages.success(self.request, "¡Autor creado exitosamente!")
        return super().form_valid(form)


class AutorUpdateView(AdminRequiredMixin, UpdateView):
    model = Autor
    fields = ['nombre', 'apellido', 'biografia', 'fecha_nacimiento', 'pais']
    template_name = 'dashboard/autores/autor_form.html'
    success_url = reverse_lazy('dashboard:autor_list')

    def form_valid(self, form):
        messages.success(self.request, "¡Autor actualizado correctamente!")
        return super().form_valid(form)


class AutorDeleteView(AdminRequiredMixin, DeleteView):
    model = Autor
    template_name = 'dashboard/autores/autor_confirm_delete.html'
    success_url = reverse_lazy('dashboard:autor_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Autor eliminado con éxito.")
        return super().delete(request, *args, **kwargs)


# CRUD DE CATEGORÍAS
class CategoriaListView(AdminRequiredMixin, ListView):
    model = Categoria
    template_name = 'dashboard/categorias/categoria_list.html'
    context_object_name = 'categorias'
    paginate_by = 10


class CategoriaCreateView(AdminRequiredMixin, CreateView):
    model = Categoria
    fields = ['nombre', 'descripcion']
    template_name = 'dashboard/categorias/categoria_form.html'
    success_url = reverse_lazy('dashboard:categoria_list')

    def form_valid(self, form):
        messages.success(self.request, "¡Categoría creada exitosamente!")
        return super().form_valid(form)


class CategoriaUpdateView(AdminRequiredMixin, UpdateView):
    model = Categoria
    fields = ['nombre', 'descripcion']
    template_name = 'dashboard/categorias/categoria_form.html'
    success_url = reverse_lazy('dashboard:categoria_list')

    def form_valid(self, form):
        messages.success(self.request, "¡Categoría actualizada correctamente!")
        return super().form_valid(form)


class CategoriaDeleteView(AdminRequiredMixin, DeleteView):
    model = Categoria
    template_name = 'dashboard/categorias/categoria_confirm_delete.html'
    success_url = reverse_lazy('dashboard:categoria_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Categoría eliminada con éxito.")
        return super().delete(request, *args, **kwargs)


# CRUD DE EDITORIALES
class EditorialListView(AdminRequiredMixin, ListView):
    model = Editorial
    template_name = 'dashboard/editoriales/editorial_list.html'
    context_object_name = 'editoriales'
    paginate_by = 10


class EditorialCreateView(AdminRequiredMixin, CreateView):
    model = Editorial
    fields = ['nombre', 'pais', 'sitio_web']
    template_name = 'dashboard/editoriales/editorial_form.html'
    success_url = reverse_lazy('dashboard:editorial_list')

    def form_valid(self, form):
        messages.success(self.request, "¡Editorial creada exitosamente!")
        return super().form_valid(form)


class EditorialUpdateView(AdminRequiredMixin, UpdateView):
    model = Editorial
    fields = ['nombre', 'pais', 'sitio_web']
    template_name = 'dashboard/editoriales/editorial_form.html'
    success_url = reverse_lazy('dashboard:editorial_list')

    def form_valid(self, form):
        messages.success(self.request, "¡Editorial actualizada correctamente!")
        return super().form_valid(form)


class EditorialDeleteView(AdminRequiredMixin, DeleteView):
    model = Editorial
    template_name = 'dashboard/editoriales/editorial_confirm_delete.html'
    success_url = reverse_lazy('dashboard:editorial_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Editorial eliminada con éxito.")
        return super().delete(request, *args, **kwargs)

class LibroListView(AdminRequiredMixin, ListView):
    model = Libro
    template_name = 'dashboard/libros/libro_list.html'
    context_object_name = 'libros'
    paginate_by = 10
    ordering = ['-id']

#ajusta en las clases siguientes que tengan los siguientes campos: titulo, descripcion, isbn, fecha_publicacion, precio_compra, precio_alquiler, stock, disponible, imagen, autor, editorial, categoria
class LibroCreateView(AdminRequiredMixin, CreateView):
    model = Libro
    fields = ['titulo', 'descripcion', 'isbn', 'fecha_publicacion', 'precio_compra', 'precio_alquiler', 'stock', 'disponible', 'imagen', 'autor', 'editorial', 'categoria']
    template_name = 'dashboard/libros/libro_form.html'
    success_url = reverse_lazy('dashboard:libro_list')

class LibroUpdateView(AdminRequiredMixin, UpdateView):
    model = Libro
    fields = ['titulo', 'descripcion', 'isbn', 'fecha_publicacion', 'precio_compra', 'precio_alquiler', 'stock', 'disponible', 'imagen', 'autor', 'editorial', 'categoria']
    template_name = 'dashboard/libros/libro_form.html'
    success_url = reverse_lazy('dashboard:libro_list')

class LibroDeleteView(AdminRequiredMixin, DeleteView):
    model = Libro
    template_name = 'dashboard/libros/libro_confirm_delete.html'
    success_url = reverse_lazy('dashboard:libro_list')

# --- MÓDULO DE PRÉSTAMOS ---

class LoanListView(AdminRequiredMixin, ListView):
    model = Loan
    template_name = 'dashboard/prestamos/prestamo_list.html'
    context_object_name = 'prestamos'
    paginate_by = 10

    def get_queryset(self):
        # Actualizar dinámicamente el estado a OVERDUE si corresponde antes de listar
        queryset = super().get_queryset()
        today = timezone.now().date()
        for prestamo in queryset.filter(status=Loan.Status.ACTIVE):
            if today > prestamo.due_date:
                prestamo.status = Loan.Status.OVERDUE
                prestamo.save(update_fields=['status'])
        return queryset


class LoanCreateView(AdminRequiredMixin, CreateView):
    model = Loan
    fields = ['user', 'book', 'due_date']
    template_name = 'dashboard/prestamos/prestamo_form.html'
    success_url = reverse_lazy('dashboard:prestamo_list')

    def get_initial(self):
        initial = super().get_initial()
        # Establecer la fecha de devolución por defecto a 14 días a partir de hoy
        initial['due_date'] = timezone.now().date() + timedelta(days=14)
        return initial

    def form_valid(self, form):
        libro = form.cleaned_data['book']
        
        # Validar que haya stock disponible del libro
        if libro.stock <= 0:
            form.add_error('book', f'El libro "{libro.titulo}" no tiene copias disponibles para préstamo.')
            return self.form_invalid(form)

        with transaction.atomic():
            # Descontar 1 del stock disponible
            libro.stock -= 1
            libro.save()
            
            response = super().form_valid(form)
            messages.success(self.request, f'Préstamo registrado exitosamente para {self.object.user.username}.')
            return response


class LoanReturnView(AdminRequiredMixin, View):
    """Vista para procesar la devolución de un libro de forma rápida."""
    
    def post(self, request, pk):
        prestamo = get_object_or_404(Loan, pk=pk)
        
        if prestamo.status == Loan.Status.RETURNED:
            messages.warning(request, 'Este préstamo ya fue devuelto anteriormente.')
            return redirect('dashboard:prestamo_list')

        with transaction.atomic():
            # Actualizar estado e incrementar stock
            prestamo.status = Loan.Status.RETURNED
            prestamo.returned_date = timezone.now().date()
            prestamo.save()

            libro = prestamo.book
            libro.stock += 1
            libro.save()

            messages.success(request, f'Devolución registrada correctamente. Se ha restaurado el stock de "{libro.titulo}".')

        return redirect('dashboard:prestamo_list')

# --- MÓDULO DE COMPRAS / VENTAS ---

class CompraListView(AdminRequiredMixin, ListView):
    model = Compra
    template_name = 'dashboard/compras/compra_list.html'
    context_object_name = 'compras'
    paginate_by = 10
    ordering = ['-fecha']


class CompraDetailView(AdminRequiredMixin, DetailView):
    model = Compra
    template_name = 'dashboard/compras/compra_detail.html'
    context_object_name = 'compra'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pre-cargar los detalles con el libro optimizado
        context['detalles'] = self.object.detalles.select_related('libro').all()
        return context


class CompraStatusUpdateView(AdminRequiredMixin, View):
    """Permite cambiar rápidamente el estado de una compra desde el dashboard."""

    def post(self, request, pk):
        compra = get_object_or_404(Compra, pk=pk)
        nuevo_estado = request.POST.get('estado')

        if nuevo_estado in dict(Compra.Estado.choices):
            compra.estado = nuevo_estado
            compra.save()
            messages.success(request, f'El estado de la compra #{compra.id} se actualizó a "{compra.get_estado_display()}".')
        else:
            messages.error(request, 'Estado no válido.')

        return redirect('dashboard:compra_detail', pk=compra.pk)

# --- MÓDULO DE Usuarips ---

class UserListView(AdminRequiredMixin, ListView):
    model = User
    template_name = 'dashboard/usuarios/usuario_list.html'
    context_object_name = 'usuarios'
    paginate_by = 10
    ordering = ['-created_at']


class UserUpdateView(AdminRequiredMixin, UpdateView):
    model = User
    fields = ['username', 'first_name', 'last_name', 'email', 'role', 'is_active']
    template_name = 'dashboard/usuarios/usuario_form.html'
    success_url = reverse_lazy('dashboard:usuario_list')

    def form_valid(self, form):
        messages.success(self.request, f'Usuario "{form.instance.username}" actualizado correctamente.')
        return super().form_valid(form)


class UserToggleActiveView(AdminRequiredMixin, View):
    """Permite activar o desactivar un usuario rápidamente."""
    
    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        
        # Evitar que el usuario logueado se desactive a sí mismo
        if user == request.user:
            messages.error(request, 'No puedes desactivar tu propia cuenta desde este panel.')
            return redirect('dashboard:usuario_list')

        user.is_active = not user.is_active
        user.save()
        
        estado_str = "activado" if user.is_active else "desactivado"
        messages.success(request, f'El usuario "{user.username}" ha sido {estado_str}.')
        return redirect('dashboard:usuario_list')