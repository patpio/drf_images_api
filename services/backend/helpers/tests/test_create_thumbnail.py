import os

from django.test import override_settings

from helpers.create_thumbnail import create_thumbnail


@override_settings(MEDIA_ROOT=(os.environ.get('TEST_DIR') + '/media'))
def test_creating_thumbnail(db, create_test_image, remove_test_data):
    image = create_test_image

    assert create_thumbnail(image, 200) == 'test_file_200.jpg'
