import factory
from django.contrib.auth.hashers import make_password

from ...users.models import CustomUser


class CustomUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser

    username = factory.Sequence(lambda n: 'user{}@test.com'.format(n))
    email = factory.LazyAttribute(
        lambda a: '{}@mail.com'.format(a.username).lower()
    )
    password = factory.LazyAttribute(lambda a: make_password(a.username))
