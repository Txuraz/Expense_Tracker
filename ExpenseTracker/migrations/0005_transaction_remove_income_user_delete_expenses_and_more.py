# Generated by Django 4.2.6 on 2023-10-10 15:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ExpenseTracker', '0004_alter_expenses_category_alter_income_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('category', models.CharField(choices=[('Income', 'Income'), ('Expenses', 'Expenses')], max_length=50)),
                ('date', models.DateField()),
                ('type', models.CharField(choices=[('Income', 'Income'), ('Expenses', 'Expenses')], max_length=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='income',
            name='user',
        ),
        migrations.DeleteModel(
            name='Expenses',
        ),
        migrations.DeleteModel(
            name='Income',
        ),
    ]
