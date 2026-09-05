from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView
from django.db.models import Avg, Q
from users.decorators import admin_required
from .forms import ReviewForm
from .models import Libro, Categoria, Autor, Editorial, Review


class CatalogHomeView(ListView):
    """
    Vista basada en clase para el catálogo general.
    Mantiene la búsqueda multifiltro (Q), filtrado por categoría y select_related.
    """
    model = Libro
    template_name = 'catalog/catalog_home.html'
    context_object_name = 'libros'
    paginate_by = 12

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resenas'] = self.object.resenas.filter(aprobada=True).select_related('usuario')
        context['review_form'] = ReviewForm()
        context['promedio_resenas'] = context['resenas'].aggregate(promedio=Avg('puntuacion'))['promedio']
        return context


@login_required
@require_POST
def review_create_view(request, book_id):
    libro = get_object_or_404(Libro, pk=book_id)
    form = ReviewForm(request.POST)
    if form.is_valid():
        review, created = Review.objects.update_or_create(
            libro=libro,
            usuario=request.user,
            defaults={**form.cleaned_data, 'aprobada': False},
        )
        message = 'Reseña enviada para moderación.' if created else 'Reseña actualizada y enviada para moderación.'
        messages.success(request, message)
    else:
        messages.error(request, 'Revisa la puntuación y el comentario de tu reseña.')
    return redirect('libro_detail', pk=libro.pk)


@login_required
@require_POST
def review_delete_view(request, review_id):
    review = get_object_or_404(Review, pk=review_id, usuario=request.user)
    libro_id = review.libro_id
    review.delete()
    messages.success(request, 'Reseña eliminada.')
    return redirect('libro_detail', pk=libro_id)


@login_required
def review_edit_view(request, review_id):
    review = get_object_or_404(Review, pk=review_id, usuario=request.user)
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            review = form.save(commit=False)
            review.aprobada = False
            review.save()
            messages.success(request, 'Reseña actualizada y enviada para moderación.')
            return redirect('libro_detail', pk=review.libro_id)
    else:
        form = ReviewForm(instance=review)
    return render(request, 'catalog/review_form.html', {'form': form, 'review': review})


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