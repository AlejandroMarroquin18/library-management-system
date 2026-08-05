from django.db import models
from django.conf import settings
from catalog.models import Libro
from datetime import timedelta
from django.utils import timezone
from core.models import TimeStampedModel


class Loan(TimeStampedModel):
    class Status(models.TextChoices):
        ACTIVE = 'ACTIVE', 'Activo'
        RETURNED = 'RETURNED', 'Devuelto'
        OVERDUE = 'OVERDUE', 'Vencido'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='loans'
    )
    book = models.ForeignKey(
        Libro, 
        on_delete=models.PROTECT, 
        related_name='loans'
    )
    loan_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    returned_date = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=10, 
        choices=Status.choices, 
        default=Status.ACTIVE
    )

    class Meta:
        ordering = ['-loan_date']
        verbose_name = 'Préstamo'
        verbose_name_plural = 'Préstamos'

    def __str__(self):
        return f"Préstamo #{self.id} - {self.book.titulo} ({self.user.username})"

    @property
    def is_overdue(self):
        """Verifica dinámicamente si el préstamo está vencido."""
        if self.status == self.Status.ACTIVE and timezone.now().date() > self.due_date:
            return True
        return False