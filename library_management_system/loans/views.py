from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError
from users.decorators import admin_required
from .services import LoanService
from .models import Loan

# VISTAS DEL USUARIO (CUSTOMER)
@login_required
def request_loan_view(request, book_id):
    """Acción para que un usuario autenticado solicite el préstamo de un libro."""
    if request.method == 'POST':
        try:
            loan = LoanService.create_loan(request.user, book_id)
            messages.success(
                request, 
                f"¡Préstamo de '{loan.book.titulo}' registrado con éxito! Fecha límite de devolución: {loan.due_date}."
            )
        except ValidationError as e:
            messages.error(request, e.message)
            
    return redirect('my_loans')


@login_required
def my_loans_view(request):
    """Listado del historial de préstamos del usuario autenticado."""
    # Actualizamos préstamos que hayan pasado la fecha límite a OVERDUE
    LoanService.update_overdue_status()

    user_loans = Loan.objects.filter(user=request.user).select_related('book')
    return render(request, 'loans/my_loans.html', {'loans': user_loans})


# VISTAS DEL ADMINISTRADOR (ADMIN)
@admin_required
def admin_loans_list_view(request):
    """Panel para que el Admin gestione todos los préstamos y aplique filtros."""
    LoanService.update_overdue_status()

    status_filter = request.GET.get('status', '').strip()
    loans = Loan.objects.all().select_related('user', 'book')

    if status_filter in [Loan.Status.ACTIVE, Loan.Status.RETURNED, Loan.Status.OVERDUE]:
        loans = loans.filter(status=status_filter)

    context = {
        'loans': loans,
        'status_filter': status_filter,
        'statuses': Loan.Status.choices
    }
    return render(request, 'loans/admin_loans_list.html', context)


@admin_required
def mark_as_returned_view(request, loan_id):
    """Acción exclusiva del Admin para registrar la devolución de un libro."""
    if request.method == 'POST':
        try:
            loan = LoanService.return_loan(loan_id)
            messages.success(request, f"Se ha registrado la devolución de '{loan.book.titulo}'. Stock restaurado.")
        except ValidationError as e:
            messages.error(request, e.message)

    return redirect('admin_loans_list')