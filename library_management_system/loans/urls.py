from django.urls import path
from .views import request_loan_view, my_loans_view, admin_loans_list_view, mark_as_returned_view

urlpatterns = [
    # Rutas de Cliente
    path('my-loans/', my_loans_view, name='my_loans'),
    path('request/<int:book_id>/', request_loan_view, name='request_loan'),
    
    # Rutas de Administración
    path('manage/', admin_loans_list_view, name='admin_loans_list'),
    path('return/<int:loan_id>/', mark_as_returned_view, name='mark_as_returned'),
]