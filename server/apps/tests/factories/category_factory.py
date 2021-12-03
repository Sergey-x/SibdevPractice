import factory

from ...summary.models.category import Category


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    type = 'INC'
    title = factory.Faker('job')
