from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('view_income', view_income, name='view_income'),
    path('add_income', add_income, name='add_income'),
    path('add_income_category', AddIncomeCategory.as_view(), name='add_income_category'),
    path('add_expense_category', AddExpenseCategory.as_view(), name='add_expense_category'),
    path('edit_income/<int:id>', edit_income, name='edit_income'),
    path('delete_income/<int:id>', delete_income, name='delete_income'),
    path('view_expense', view_expense, name='view_expense'),
    path('add_expense', add_expense, name='add_expense'),
    path('edit_expense/<int:id>', edit_expense, name='edit_expense'),
    path('delete_expense/<int:id>', delete_expense, name='delete_expense'),

]