import json
import os

import factory
import pytz
from django.contrib.auth.hashers import make_password
from django.core.management import call_command
from factory.fuzzy import FuzzyChoice

from users import models


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.CustomUser

    password = make_password('testpass123')
    username = factory.Faker('user_name')
    date_joined = factory.Faker('iso8601', tzinfo=pytz.utc)
    tier = FuzzyChoice([1, 2, 3])


def run():
    os.makedirs(os.path.join('users', 'fixtures'), exist_ok=True)

    data = []

    with open(os.path.join('users', 'fixtures', 'users.json'), 'w') as f:
        for i in range(10):
            record = {
                'model': 'users.customuser',
                'fields': factory.build(dict, FACTORY_CLASS=UserFactory)
            }

            data.append(record)

        json.dump(data, f)

    call_command('loaddata', 'users.json')
