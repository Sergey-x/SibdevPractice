import factory

from ...summary.models.transaction import Transaction


class TransactionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Transaction

    sum = 50000.00
