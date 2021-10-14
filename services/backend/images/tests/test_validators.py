import os

import pytest
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings

from images.validators import validate_file_type


@override_settings(MEDIA_ROOT=(os.environ.get('TEST_DIR') + '/media'))
def test_valid_image(remove_test_data):
    image = SimpleUploadedFile('test_image.jpg',
                               content=open(os.path.join('tests', 'test_image.jpg'), 'rb').read())

    assert not validate_file_type(image)


@override_settings(MEDIA_ROOT=(os.environ.get('TEST_DIR') + '/media'))
def test_not_valid_image(remove_test_data):
    image = SimpleUploadedFile('test_file.txt', b'test not valid file type')

    with pytest.raises(ValidationError) as excinfo:
        validate_file_type(image)
    exception_msg = excinfo.value.args[0]

    assert exception_msg == 'File type not supported. Use: jpeg, png'
