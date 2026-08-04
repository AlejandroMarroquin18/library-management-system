from django.db import models

# Create your models here.

# Clase Autor. Guarda información sobre los autores de los libros.
class Autor(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    biografia = models.TextField(blank=True, null=True, verbose_name="Biografía")
    fecha_nacimiento = models.DateField(blank=True, null=True, verbose_name="Fecha de nacimiento")
    pais = models.CharField(max_length=100, blank=True, null=True, verbose_name="País")

    class Meta:
        verbose_name = "Autor"
        verbose_name_plural = "Autores"
        ordering = ['apellido', 'nombre']

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

# Clase Editorial. Guarda información sobre las editoriales de los libros.
class Editorial(models.Model):
    nombre = models.CharField(max_length=150)
    pais = models.CharField(max_length=100, blank=True, null=True, verbose_name="País")
    sitio_web = models.URLField(blank=True, null=True, verbose_name="Sitio web")

    class Meta:
        verbose_name = "Editorial"
        verbose_name_plural = "Editoriales"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

# Clase Categoria. Guarda información sobre las categorías de los libros.
class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

# Clase Libro. Guarda información sobre los libros disponibles en la librería.
class Libro(models.Model):
    titulo = models.CharField(max_length=200, verbose_name="Título")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")
    isbn = models.CharField(max_length=13, unique=True, verbose_name="ISBN")
    fecha_publicacion = models.DateField(blank=True, null=True, verbose_name="Fecha de publicación")
    
    # Precios
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio de compra")
    precio_alquiler = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio de alquiler")
    
    # Inventario y estado
    stock = models.PositiveIntegerField(default=0)
    disponible = models.BooleanField(default=True)
    
    # Archivo multimedia 
    imagen = models.ImageField(upload_to='libros/', blank=True, null=True)

    # Claves foráneas
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE, related_name='libros')
    editorial = models.ForeignKey(Editorial, on_delete=models.SET_NULL, null=True, blank=True, related_name='libros')
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name='libros', verbose_name="Categoría")

    class Meta:
        verbose_name = "Libro"
        verbose_name_plural = "Libros"
        ordering = ['titulo']

    def __str__(self):
        return self.titulo