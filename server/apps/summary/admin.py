from django.contrib import admin

from .models.category import Category
from .models.transaction import Transaction


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    pass
