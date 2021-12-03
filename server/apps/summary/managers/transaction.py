from datetime import datetime
from decimal import Decimal
from typing import Union

from django.conf import settings
from django.db import models

from ..models.category import Category


class TransactionQuerySet(models.QuerySet):
    def personal(self, owner):
        """
        Get all user's transactions.
        """
        return self.filter(owner=owner)

    def from_period(self, start_date, end_date):
        """
        Get all transactions from date interval.
        """
        queryset = self.filter(
            operation_date__gte=start_date,
            operation_date__lt=end_date,
        )
        return queryset

    def income(self):
        """
        Get all profitable transactions.
        """
        queryset = self.select_related('category').filter(
            category__type=Category.INCOME
        )
        return queryset

    def expense(self):
        """
        Get all unprofitable transactions.
        """
        queryset = self.select_related('category').filter(
            category__type=Category.EXPENSE
        )
        return queryset

    def full_sum(self):
        """
        Return sum of all transactions or 0 if transactions don't exist.
        """
        queryset = self.values('sum').aggregate(models.Sum('sum'))
        return queryset['sum__sum'] or 0

    def income_sum_for_period(self, owner, start_date, end_date):
        """
        Encapsulate functionality of getting sum of all user's profitable
        transactions from date period.
        """
        queryset = self.personal(owner).from_period(start_date, end_date)
        queryset = queryset.income().full_sum()
        return queryset

    def expense_sum_for_period(self, owner, start_date, end_date):
        """
        Encapsulate functionality of getting sum of all user's unprofitable
        transactions from date period.
        """
        queryset = self.personal(owner).from_period(start_date, end_date)
        queryset = queryset.expense().full_sum()
        return queryset


class CustomTransactionManager(models.Manager):
    def get_queryset(self):
        return TransactionQuerySet(self.model, using=self._db)

    def personal(self, owner: settings.AUTH_USER_MODEL) -> models.QuerySet:
        return self.get_queryset().personal(owner)

    def from_period(self, start_date, end_date) -> models.QuerySet:
        return self.get_queryset().from_period(start_date, end_date)

    def income(self) -> models.QuerySet:
        return self.get_queryset().income()

    def expense(self) -> models.QuerySet:
        return self.get_queryset().expense()

    def full_sum(self) -> Union[Decimal, int]:
        return self.get_queryset().full_sum()

    def income_sum_for_period(
        self,
        owner: settings.AUTH_USER_MODEL,
        start_date: datetime,
        end_date: datetime,
    ) -> models.QuerySet:
        return self.get_queryset().income_sum_for_period(
            owner=owner,
            start_date=start_date,
            end_date=end_date,
        )

    def expense_sum_for_period(
        self,
        owner: settings.AUTH_USER_MODEL,
        start_date: datetime,
        end_date: datetime,
    ) -> models.QuerySet:
        return self.get_queryset().expense_sum_for_period(
            owner=owner,
            start_date=start_date,
            end_date=end_date,
        )


TransactionManager = CustomTransactionManager.from_queryset(TransactionQuerySet)
