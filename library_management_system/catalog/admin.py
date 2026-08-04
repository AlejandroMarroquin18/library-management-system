from django.contrib import admin
from .models import Autor, Editorial, Categoria, Libro

class AutorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'pais', 'fecha_nacimiento')
    search_fields = ('nombre', 'apellido', 'pais')

class EditorialAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'pais', 'sitio_web')
    search_fields = ('nombre',)

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)

class LibroAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'categoria', 'precio_compra', 'precio_alquiler', 'stock', 'disponible')
    list_filter = ('disponible', 'categoria', 'editorial')
    search_fields = ('titulo', 'isbn', 'autor__nombre', 'autor__apellido')
    list_editable = ('precio_compra', 'precio_alquiler', 'stock', 'disponible')

admin.site.register(Autor, AutorAdmin)
admin.site.register(Editorial, EditorialAdmin) 
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Libro, LibroAdmin)