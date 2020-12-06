from django.db import models
from django.db.models import Sum
from django.utils.timezone import now

from .managers import GeneralManager

try:
    from ..users.models import User
except (ValueError, ImportError):
    from users.models import User

CURRENCY = '₹'


class IncomeCategory(models.Model):

    name = models.CharField(unique=True, max_length=255)

    class Meta:
        verbose_name_plural = 'Income category'

    def __str__(self):
        return self.name


class Income(models.Model):
    description = models.CharField(max_length=100, blank=True, null=True)
    date_received = models.DateField()
    amount = models.DecimalField(default=0, decimal_places=2, max_digits=20)
    owner = models.ForeignKey(to=User, null=True, on_delete=models.CASCADE)
    category = models.CharField(max_length=255)

    def __str__(self):
        return self.description + '|' + str(self.category)

    class Meta:
        ordering = ['-date_received']
        verbose_name_plural = 'Incomes'


class ExpenseCategory(models.Model):
    name = models.CharField(unique=True, max_length=255)

    class Meta:
        verbose_name_plural = 'Expense category'

    def __str__(self):
        return self.name


class Expense(models.Model):
    note = models.CharField(max_length=100, blank=True, null=True)
    date_paid = models.DateField()
    amount = models.DecimalField(default=0, decimal_places=2, max_digits=20)
    owner = models.ForeignKey(to=User, null=True, on_delete=models.CASCADE)
    category = models.CharField(max_length=255)

    def __str__(self):
        return self.note + '|' + str(self.category)

    class Meta:
        ordering = ['-date_paid']
        verbose_name_plural = 'Expenses'

    def tag_category(self):
        return f'{self.category}'
