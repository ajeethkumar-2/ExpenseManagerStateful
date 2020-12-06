from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
#from matplotlib import pyplot as plt
from .models import *
from django.contrib import messages
from django.core.paginator import Paginator

try:
    from ..EM import settings
except (ValueError, ImportError):
    from EM import settings

CURRENCY = settings.CURRENCY


def home(request):
    if request.user.is_authenticated:
        income_items = Income.objects.filter(owner=request.user).order_by('-date_received')
        expense_items = Expense.objects.filter(owner=request.user).order_by('-date_paid')
        currency = CURRENCY

        try:
            income_total = Income.objects.filter(owner=request.user).aggregate(
                income=Sum('amount', filter=Q(amount__gt=0)))
            expense_total = Expense.objects.filter(owner=request.user).aggregate(
                expense=Sum('amount', filter=Q(amount__gt=0)))

            if income_total['income'] is None:
                income_total['income'] = 0

            if expense_total['expense'] is None:
                expense_total['expense'] = 0

            '''fig, ax = plt.subplot(ncols=2)
            ax.bar(['Income', 'Expense'], [abs(income_total['income']), abs(expense_total['expense'])], color=['green', 'red'])
            ax.set_title('Your Total Income vs Total Expense')
            plt.savefig('EM/static/chart/expense.jpg')'''

        except TypeError:
            print('No data.')
        context = {
            'income_items': income_items,
            'expense_items': expense_items,
            'income': abs(income_total['income']),
            'expense': abs(expense_total['expense']),
            'currency': currency
            }

        return render(request, 'home.html', context)
    else:
        return redirect('login')


def view_income(request):
    incomes = Income.objects.filter(owner=request.user)
    categories = IncomeCategory.objects.all()
    paginator = Paginator(incomes, 2)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    context = {
        'categories': categories,
        'incomes': incomes,
        'page_obj': page_obj,
    }

    return render(request, 'tracker/view_income.html', context)


class AddIncomeCategory(CreateView):
    model = IncomeCategory
    template_name = 'tracker/add_income_category.html'
    fields = '__all__'
    success_url = reverse_lazy('add_income')

    def get_context_data(self, *args, **kwargs):
        cat_menu = IncomeCategory.objects.all()
        context = super(AddIncomeCategory, self).get_context_data(*args, **kwargs)
        context['cat_menu'] = cat_menu
        return context


def add_income(request):
    categories = IncomeCategory.objects.all()
    income_items = Income.objects.filter(owner=request.user).order_by('-date_received')
    expense_items = Expense.objects.filter(owner=request.user).order_by('-date_paid')
    try:
        income_total = Income.objects.filter(owner=request.user).aggregate(
            income=Sum('amount', filter=Q(amount__gt=0)))
        expense_total = Expense.objects.filter(owner=request.user).aggregate(
            expense=Sum('amount', filter=Q(amount__gt=0)))

        if income_total['income'] is None:
            income_total['income'] = 0

        if expense_total['expense'] is None:
            expense_total['expense'] = 0

        '''fig, ax = plt.subplot(ncols=2)
        ax.bar(['Income', 'Expense'], [abs(income_total['income']), abs(expense_total['expense'])],
               color=['green', 'red'])
        ax.set_title('Your Total Income vs Total Expense')
        plt.savefig('EM/static/chart/expense.jpg')'''
    except TypeError:
        print('No data.')
        
    context = {
        'categories': categories,
        'values': request.POST,
        'income_items': income_items,
        'expense_items': expense_items,
        'income': abs(income_total['income']),
        'expense': abs(expense_total['expense']),
    }
    if request.method == 'GET':
        return render(request, 'tracker/add_income.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        date_received = request.POST['date_received']
        category = request.POST['category']

        if not amount:
            messages.error(request, 'Amount Field is Required')
            return render(request, 'tracker/add_income.html', context)

        if not description:
            messages.error(request, 'Description Field is Required')
            return render(request, 'tracker/add_income.html', context)

        if not date_received:
            messages.error(request, 'Date Field is Required')
            return render(request, 'tracker/add_income.html', context)

        if not category:
            messages.error(request, 'Category Field is Required')
            return render(request, 'tracker/add_income.html', context)

        Income.objects.create(owner=request.user, amount=amount,
                              description=description, date_received=date_received,
                              category=category,
                            )
        messages.success(request, 'Income added SuccessFully...!!!')

        return redirect('view_income')


def edit_income(request, id):
    categories = IncomeCategory.objects.all()
    income = Income.objects.get(pk=id)
    context = {
        'categories': categories,
        'income': income,
        'values': request.POST
    }
    if request.method == 'GET':
        return render(request, 'tracker/edit_income.html', context)

        if request.method == 'POST':
            amount = request.POST['amount']
            description = request.POST['description']
            date_received = request.POST['date_received']
            category = request.POST['category']

            if not amount:
                messages.error(request, 'Amount Field is Required')
                return render(request, 'tracker/add_income.html', context)

            if not description:
                messages.error(request, 'Description Field is Required')
                return render(request, 'tracker/add_income.html', context)

            if not date_received:
                messages.error(request, 'Date Field is Required')
                return render(request, 'tracker/add_income.html', context)

            if not category:
                messages.error(request, 'Category Field is Required')
                return render(request, 'tracker/add_income.html', context)

        income.owner = request.user
        income.amount = amount
        income.category = category
        income.description = description
        income.date_received = date_received

        income.save()
        messages.success(request, 'Income Edited SuccessFully...!!!')
        return redirect('view_income')


def delete_income(request, id):
    income = Income.objects.get(pk=id)
    income.delete()
    messages.success(request, 'Income Deleted SuccessFully...!!!')
    return redirect('view_income')


def view_expense(request):
    expenses = Expense.objects.filter(owner=request.user)
    categories = ExpenseCategory.objects.all()
    paginator = Paginator(expenses, 2)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    context = {
        'categories': categories,
        'expenses': expenses,
        'page_obj': page_obj,
    }
    return render(request, 'tracker/view_expense.html', context)


class AddExpenseCategory(CreateView):
    model = ExpenseCategory
    template_name = 'tracker/add_expense_category.html'
    fields = '__all__'
    success_url = reverse_lazy('add_expense')

    def get_context_data(self, *args, **kwargs):
        cat_menu = ExpenseCategory.objects.all()
        context = super(AddExpenseCategory, self).get_context_data(*args, **kwargs)
        context['cat_menu'] = cat_menu
        return context


def add_expense(request):
    categories = ExpenseCategory.objects.all()
    context = {
        'categories': categories,
        'values': request.POST
    }
    if request.method == 'GET':
        return render(request, 'tracker/add_expense.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']
        note = request.POST['note']
        date_paid = request.POST['date_paid']
        category = request.POST['category']

        if not amount:
            messages.error(request, 'Amount Field is Required')
            return render(request, 'tracker/add_income.html', context)

        if not note:
            messages.error(request, 'Note Field is Required')
            return render(request, 'tracker/add_income.html', context)

        if not date_paid:
            messages.error(request, 'Date Field is Required')
            return render(request, 'tracker/add_income.html', context)

        if not category:
            messages.error(request, 'Category Field is Required')
            return render(request, 'tracker/add_income.html', context)

        Expense.objects.create(owner=request.user, amount=amount, note=note,
                               date_paid=date_paid,
                               category=category)
        messages.success(request, 'Expense added SuccessFully...!!!')

        return redirect('view_expense')


def edit_expense(request, id):
    categories = ExpenseCategory.objects.all()
    expense = Expense.objects.get(pk=id)
    context = {
        'categories': categories,
        'expense': expense,
        'values': request.POST
    }
    if request.method == 'GET':
        return render(request, 'tracker/edit_expense.html', context)

        if request.method == 'POST':
            amount = request.POST['amount']
            note = request.POST['note']
            date_paid = request.POST['date_paid']
            category = request.POST['category']

            if not amount:
                messages.error(request, 'Amount Field is Required')
                return render(request, 'tracker/edit_expense.html', context)

            if not note:
                messages.error(request, 'Description Field is Required')
                return render(request, 'tracker/edit_expense.html', context)

            if not date_paid:
                messages.error(request, 'Date Field is Required')
                return render(request, 'tracker/edit_expense.html', context)

            if not category:
                messages.error(request, 'Category Field is Required')
                return render(request, 'tracker/edit_expense.html', context)

        expense.owner = request.user
        expense.amount = amount
        expense.category = category
        expense.note = note
        expense.date_paid = date_paid

        expense.save()
        messages.success(request, 'Expense Edited SuccessFully...!!!')
        return redirect('view_expense')


def delete_expense(request, id):
    expense = Expense.objects.get(pk=id)
    expense.delete()
    messages.success(request, 'Expense Deleted SuccessFully...!!!')
    return redirect('view_expense')
