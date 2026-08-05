from django.contrib import admin
from .models import Loan

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'book', 'loan_date', 'due_date', 'returned_date', 'status')
    list_filter = ('status', 'loan_date', 'due_date')
    search_fields = ('user__username', 'book__titulo', 'id')
    readonly_fields = ('loan_date',)