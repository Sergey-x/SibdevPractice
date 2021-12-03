# Generated by Django 3.2.2 on 2021-08-16 14:16

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('INC', 'Income'), ('EXP', 'Expense')], max_length=3, verbose_name='category type')),
                ('title', models.CharField(max_length=64, verbose_name='category title')),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sum', models.DecimalField(decimal_places=10, max_digits=26, verbose_name='monetary amount of the transaction')),
                ('operation_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date when transaction was made')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='summary.category', verbose_name='transaction category')),
            ],
            options={
                'ordering': ['operation_date'],
            },
        ),
    ]