from decimal import Decimal

from django.db import models
from django.db.models.functions import Coalesce


class CategoryQuerySet(models.QuerySet):
    """
    Annotate each category object with sum of all bound transactions
    or 0 if transactions don't exist.
    """

    def with_sum(self):
        return self.annotate(
            sum=Coalesce(
                models.Sum('transaction__sum'),
                Decimal(0),
            )
        )


class CustomCategoryManager(models.Manager):
    def get_queryset(self) -> CategoryQuerySet:
        return CategoryQuerySet(self.model, using=self._db)

    def with_sum(self) -> models.QuerySet:
        return self.get_queryset().with_sum()


CategoryManager = CustomCategoryManager.from_queryset(CategoryQuerySet)
