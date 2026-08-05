from django.db import models

# Create your models here.


class TimeStampedModel(models.Model):
    """
    Modelo base abstracto que añade timestamps de creación y actualización
    a todos los modelos que hereden de él.
    """
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    class Meta:
        abstract = True