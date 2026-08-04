from django.db import transaction
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
from .models import Loan
from catalog.models import Libro


class LoanService:
    DEFAULT_LOAN_DAYS = 14  # Plazo estándar de 14 días para la devolución

    @staticmethod
    @transaction.atomic
    def create_loan(user, book_id):
        """
        Solicita un préstamo para un libro determinado.
        Descuenta 1 unidad del stock.
        """
        book = Libro.objects.select_for_update().get(id=book_id)

        # 1. Reglas de validación previa
        if not book.disponible:
            raise ValidationError(f"El libro '{book.titulo}' no está disponible para préstamos.")
        
        if book.stock < 1:
            raise ValidationError(f"No hay unidades disponibles en stock de '{book.titulo}'.")

        # 2. Verificar si el usuario ya tiene este mismo libro en préstamo activo
        active_same_book = Loan.objects.filter(
            user=user, 
            book=book, 
            status__in=[Loan.Status.ACTIVE, Loan.Status.OVERDUE]
        ).exists()

        if active_same_book:
            raise ValidationError(f"Ya tienes un préstamo activo del libro '{book.titulo}'.")

        # 3. Disminuir stock
        book.stock -= 1
        book.save()

        # 4. Crear el registro de préstamo
        today = timezone.now().date()
        loan = Loan.objects.create(
            user=user,
            book=book,
            loan_date=today,
            due_date=today + timedelta(days=LoanService.DEFAULT_LOAN_DAYS),
            status=Loan.Status.ACTIVE
        )

        return loan

    @staticmethod
    @transaction.atomic
    def return_loan(loan_id):
        """
        Registra la devolución de un préstamo (Acción del Administrador).
        Aumenta 1 unidad al stock.
        """
        loan = Loan.objects.select_for_update().get(id=loan_id)

        if loan.status == Loan.Status.RETURNED:
            raise ValidationError("Este préstamo ya fue devuelto anteriormente.")

        # 1. Aumentar stock del libro
        book = loan.book
        book.stock += 1
        book.save()

        # 2. Actualizar el estado del préstamo
        loan.returned_date = timezone.now().date()
        loan.status = Loan.Status.RETURNED
        loan.save()

        return loan

    @staticmethod
    def update_overdue_status():
        """
        Helper para actualizar automáticamente el estado a OVERDUE 
        si ya pasó la fecha límite de devolución.
        """
        today = timezone.now().date()
        Loan.objects.filter(
            status=Loan.Status.ACTIVE, 
            due_date__lt=today
        ).update(status=Loan.Status.OVERDUE)