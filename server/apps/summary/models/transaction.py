from django.conf import settings
from django.db import models
from django.utils import timezone

from ..managers.transaction import TransactionManager
from .category import Category


class Transaction(models.Model):
    """
    Model for financial accounting.
    """
    owner = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="user who made transaction",
    )
    category = models.ForeignKey(
        to=Category,
        on_delete=models.PROTECT,
        verbose_name="transaction category",
    )
    sum = models.DecimalField(
        max_digits=26,
        decimal_places=10,
        verbose_name="monetary amount of the transaction",
    )
    operation_date = models.DateTimeField(
        default=timezone.now,
        verbose_name="date when transaction was made",
    )

    class Meta:
        indexes = [
            models.Index(fields=['owner']),
            models.Index(fields=['owner', 'operation_date']),
        ]
        ordering = ['operation_date']
        app_label = 'summary'

    objects = TransactionManager()

    @property
    def category_type(self):
        return self.category.type
