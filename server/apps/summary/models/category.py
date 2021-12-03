from django.conf import settings
from django.db import models

from ..managers.category import CategoryManager


class Category(models.Model):
    """
    Transaction category model.
    """
    INCOME = 'INC'
    EXPENSE = 'EXP'
    CATEGORY_TYPES = [
        (INCOME, 'Income'),
        (EXPENSE, 'Expense'),
    ]

    type = models.CharField(
        verbose_name="category type",
        choices=CATEGORY_TYPES,
        max_length=3,
    )
    title = models.CharField(verbose_name="category title", max_length=64)
    owner = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="category creator",
    )

    class Meta:
        indexes = [
            models.Index(fields=['owner']),
        ]
        unique_together = ['type', 'title', 'owner']
        ordering = ['title']
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        app_label = 'summary'

    objects = CategoryManager()

    def __str__(self):
        return self.title
