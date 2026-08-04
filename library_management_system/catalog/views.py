from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Q
from users.decorators import admin_required
from .models import Libro, Categoria, Autor, Editorial


class CatalogHomeView(ListView):
    """
    Vista basada en clase para el catálogo general.
    Mantiene la búsqueda multifiltro (Q), filtrado por categoría y select_related.
    """
    model = Libro
    template_name = 'catalog/catalog_home.html'
    context_object_name = 'libros'

    def get_queryset(self):
        # Base QuerySet con la optimización JOIN de autor y categoría
        queryset = Libro.objects.filter(disponible=True).select_related('autor', 'categoria')

        # --- BÚSQUEDA ---
        search_query = self.request.GET.get('q', '').strip()
        if search_query:
            queryset = queryset.filter(
                Q(titulo__icontains=search_query) |
                Q(autor__nombre__icontains=search_query) |
                Q(autor__apellido__icontains=search_query) |
                Q(isbn__icontains=search_query)
            )

        # --- FILTRAR POR CATEGORÍA ---
        categoria_id = self.request.GET.get('categoria')
        if categoria_id and categoria_id.isdigit():
            queryset = queryset.filter(categoria_id=int(categoria_id))

        return queryset

    def get_context_data(self, **kwargs):
        """Pasa las variables adicionales necesarias a la plantilla."""
        context = super().get_context_data(**kwargs)
        
        search_query = self.request.GET.get('q', '').strip()
        categoria_id = self.request.GET.get('categoria')

        context['categorias'] = Categoria.objects.all()
        context['search_query'] = search_query
        context['categoria_seleccionada'] = int(categoria_id) if categoria_id and categoria_id.isdigit() else None
        
        return context


class LibroDetailView(DetailView):
    """
    Vista de detalle de un libro optimizada.
    Aprovecha select_related para evitar N+1 queries al cargar relaciones.
    """
    model = Libro
    template_name = 'catalog/libro_detail.html'
    context_object_name = 'libro'

    def get_queryset(self):
        return Libro.objects.select_related('autor', 'categoria')


# VISTA PRIVADA: Solo accesible para el ADMIN
@admin_required
def libro_create(request):
    """
    Vista de administración para añadir libros directamente desde la app.
    Un CUSTOMER que intente entrar aquí recibirá un error HTTP 403.
    """
    if request.method == 'POST':
        # Aquí procesaremos el formulario de creación de libro
        pass
    
    return render(request, 'catalog/libro_form.html')