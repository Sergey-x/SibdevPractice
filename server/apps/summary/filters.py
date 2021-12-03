from datetime import datetime
from decimal import Decimal

from django.db import models
from django.db.models.functions import Coalesce
from django_filters import rest_framework as filters


class DateIntervalFilter(filters.FilterSet):
    start_date = filters.DateTimeFilter(
        field_name='operation_date',
        lookup_expr='gte',
    )
    end_date = filters.DateTimeFilter(
        field_name='operation_date',
        lookup_expr='lt',
    )


class DateIntervalFilterForCategory(filters.FilterSet):
    @property
    def qs(self):
        parent_qs = super().qs
        start_data = self.data.get('start_date', datetime.fromisoformat('1900-01-01'))
        end_date = self.data.get('end_date', datetime.now())

        return parent_qs.annotate(
            sum=Coalesce(
                models.Sum(
                    'transaction__sum',
                    filter=models.Q(
                        transaction__operation_date__gte=start_data,
                        transaction__operation_date__lt=end_date,
                    ),
                ),
                Decimal(0),
            ),
        )
