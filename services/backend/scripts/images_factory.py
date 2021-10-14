import factory
from factory.fuzzy import FuzzyChoice, FuzzyInteger

from images.models import Image
from users.models import CustomUser


users = list(CustomUser.objects.all())


class ImageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Image

    author = FuzzyChoice(users)
    name = factory.Faker('file_name', extension=FuzzyChoice(['jpg', 'png']))
    url = factory.django.ImageField(filename=name,
                                    color=FuzzyChoice(['yellow', 'green', 'red']),
                                    width=FuzzyInteger(600, 1000),
                                    height=FuzzyInteger(600, 1000)
                                    )


def run():
    for i in range(10):
        ImageFactory()
