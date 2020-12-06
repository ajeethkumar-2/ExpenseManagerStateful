from django import forms
from .models import *


income_category_choices = IncomeCategory.objects.all().values_list('name', 'name')
income_category_choices_list = []
for item in income_category_choices:
    income_category_choices_list.append(item)

expense_category_choices = ExpenseCategory.objects.all().values_list('name', 'name')
expense_category_choices_list = []
for item in expense_category_choices:
    expense_category_choices_list.append(item)


class AddIncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ('amount', 'category', 'description', 'date_received')

        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control', }),
            'category': forms.Select(choices=income_category_choices, attrs={'class': 'form-control'}),
            'date_received': forms.DateInput(attrs={'class': 'form-control-file'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }


class AddExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ('amount', 'category', 'note', 'date_paid')

        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control', }),
            'category': forms.Select(choices=income_category_choices, attrs={'class': 'form-control'}),
            'date_paid': forms.DateInput(attrs={'class': 'form-control-file'}),
            'note': forms.Textarea(attrs={'class': 'form-control'}),
        }