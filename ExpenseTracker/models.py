# models.py

from django.db import models
from django.contrib.auth.models import User

class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('Income', 'Income'),
        ('Expenses', 'Expenses'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50, choices=TRANSACTION_TYPES)
    type = models.CharField(max_length=50, choices=TRANSACTION_TYPES)
    date = models.DateField()

    def is_income(self):
        return self.category == 'Income'

    def is_expense(self):
        return self.category == 'Expenses'

    def get_type(self):
        return self.category


