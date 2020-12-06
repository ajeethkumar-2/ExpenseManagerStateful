from django.db import models
from django.db.models import Sum
from django.utils.timezone import now
try:
    from ..users.models import User
except (ValueError, ImportError):
    from users.models import User

CURRENCY = '₹'


class Income(models.Model):
    amount = models.FloatField()
    date_received = models.DateField(default=now)
    description = models.TextField()
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    category = models.CharField(max_length=255)

    def __str__(self):
        return self.description + '|' + str(self.category)

    class Meta:
        ordering = ['-date_received']
        verbose_name_plural = 'Incomes'

    def tag_final_value(self):
        return f'{CURRENCY} {self.amount}'

    tag_final_value.short_description = 'Value'

    @staticmethod
    def analysis(queryset):
        amount = queryset.aggregate(Sum('amount'))['amount__sum'] if queryset else 0
        category_analysis = queryset.values('category__title').annotate(amount=Sum('amount'))
        return [amount, category_analysis]

    @staticmethod
    def filters_data(request, queryset):
        search_name = request.GET.get('search_name', None)
        cate_name = request.GET.getlist('cate_name', None)

        queryset = queryset.filter(description__icontains=search_name) if search_name else queryset
        queryset = queryset.filter(category__id__in=cate_name) if cate_name else queryset
        return queryset


class IncomeCategory(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Income Categories'

    def __str__(self):
        return self.name


class Expense(models.Model):
    amount = models.FloatField()
    date_paid = models.DateField(default=now)
    description = models.TextField()
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    category = models.CharField(max_length=255)

    def __str__(self):
        return self.description + '|' + str(self.category)

    class Meta:
        ordering = ['-date_paid']
        verbose_name_plural = 'Expenses'

    def tag_final_value(self):
        return f'{CURRENCY} {self.amount}'

    tag_final_value.short_description = 'Value'

    @staticmethod
    def analysis(queryset):
        amount = queryset.aggregate(Sum('amount'))['amount__sum'] if queryset else 0
        category_analysis = queryset.values('category__title').annotate(amount=Sum('amount'))
        return [amount, category_analysis]

    @staticmethod
    def filters_data(request, queryset):
        search_name = request.GET.get('search_name', None)
        cate_name = request.GET.getlist('cate_name', None)

        queryset = queryset.filter(description__icontains=search_name) if search_name else queryset
        queryset = queryset.filter(category__icontains=cate_name) if cate_name else queryset
        return queryset


class ExpenseCategory(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Expense Categories'

    def __str__(self):
        return self.name