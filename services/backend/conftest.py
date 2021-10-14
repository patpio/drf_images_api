import os
import shutil
from uuid import uuid4

import pytest
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings

from expiring_links.models import ExpiringLink
from images.models import Image, Thumbnail
from tiers.models import Tier, Size


@pytest.fixture(scope='function')
def remove_test_data():
    yield
    try:
        shutil.rmtree(os.environ.get('TEST_DIR'))
    except OSError:
        pass


@pytest.fixture()
def api_rf():
    from rest_framework.test import APIRequestFactory
    return APIRequestFactory()


@pytest.fixture(scope='function')
def create_test_size():
    size = Size.objects.create(
        height=200
    )
    return size


@pytest.fixture(scope='function')
def create_test_tier(create_test_size):
    tier = Tier.objects.create(
        name='test tier',
        expired_link_flag=True
    )
    tier.size.add(create_test_size)
    return tier


@pytest.fixture(scope='function')
def create_test_user(create_test_tier):
    user = get_user_model().objects.create_user(
        username='testuser',
        password='testpass123',
        tier=create_test_tier
    )
    return user


@pytest.fixture(scope='function')
@override_settings(MEDIA_ROOT=(os.environ.get('TEST_DIR') + '/media'))
def create_test_image(create_test_user):
    image = Image.objects.create(
        author=create_test_user,
        url=SimpleUploadedFile('test_file.jpg',
                               content=open(os.path.join('tests', 'test_image.jpg'), 'rb').read())
    )
    return image


@pytest.fixture(scope='function')
@override_settings(MEDIA_ROOT=(os.environ.get('TEST_DIR') + '/media'))
def create_test_thumbnail(create_test_image):
    thumbnail = Thumbnail.objects.create(
        image=create_test_image,
        url=SimpleUploadedFile('test_resized_file.jpg',
                               content=open(os.path.join('tests', 'test_image.jpg'), 'rb').read()),
        height=200
    )
    return thumbnail


@pytest.fixture(scope='function')
def create_test_thumbnail_serializer_data(create_test_image):
    serializer_data = {
        'image_id': create_test_image.pk,
        'heights': [200]
    }
    return serializer_data


@pytest.fixture(scope='function')
def create_test_expiring_link():
    expiring_link = ExpiringLink.objects.create(
        url='http://test_link.com',
        token=uuid4(),
        duration=350
    )
    return expiring_link


@pytest.fixture(scope='function')
def create_test_expiring_link_serializer_data(create_test_image):
    serializer_data = {
        'image_id': create_test_image.pk,
        'expiration_time': 350
    }
    return serializer_data
