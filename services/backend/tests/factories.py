import factory

from tiers.models import Size, Tier
from users.models import CustomUser


class TestUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser

    username = 'testuser'
    password = 'testpass123'


class TestSizeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Size

    height = 200


class TestTierFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tier

    name = 'test tier'
