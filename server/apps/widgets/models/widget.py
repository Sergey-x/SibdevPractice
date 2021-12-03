from django.conf import settings
from django.db import models
from django.utils import timezone


class Widget(models.Model):
    owner = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='user who create widget',
    )

    category = models.ForeignKey(
        to='summary.Category',
        on_delete=models.PROTECT,
        verbose_name='tracked category',
    )

    limit = models.DecimalField(
        verbose_name='max sum that user can spend',
        max_digits=26,
        decimal_places=5,
    )

    VALID_DURATION = (1, 7, 30)
    duration = models.DurationField(
        verbose_name='validity period of widget (in days)',
    )

    MORE = 'M'
    LESS = 'L'
    CRITERIA_TYPES = [
        (MORE, 'More'),
        (LESS, 'Less'),
    ]
    criteria = models.CharField(
        verbose_name='spending control criteria',
        choices=CRITERIA_TYPES,
        max_length=1,
    )

    color = models.CharField(
        verbose_name='color of widget',
        max_length=8,
        default='ffffffff',  # white opaque color
    )

    creation_date = models.DateTimeField(
        default=timezone.now,
        verbose_name="date when widget was created",
    )

    class Meta:
        verbose_name = 'widget'
        verbose_name_plural = 'widgets'
        ordering = ['-creation_date']
        app_label = 'widgets'

    @property
    def ending_date(self):
        return self.creation_date + self.duration

    @property
    def sum(self):
        return self.category.transaction_set.all().filter(
            operation_date__gte=self.creation_date,
            operation_date__lt=self.ending_date,
        ).full_sum()
