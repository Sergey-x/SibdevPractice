from datetime import timedelta

import factory

from ...widgets.models.widget import Widget


class WidgetFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Widget

    limit = 1000000.00
    duration = timedelta(days=1)
    criteria = 'M'
