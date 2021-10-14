import pytest

from images.models import Thumbnail


@pytest.mark.models
def test_thumbnail_creation(db, create_test_thumbnail, create_test_image, remove_test_data):
    assert isinstance(create_test_thumbnail, Thumbnail)
    assert create_test_thumbnail.image == create_test_image
    assert create_test_thumbnail.url.url == '/media/resized_images/test_resized_file.jpg'
    assert create_test_thumbnail.height == 200
    assert create_test_thumbnail.__str__(), 'resized_images/test_resized_file.jpg'


@pytest.mark.models
def test_thumbnail_fields(db, create_test_thumbnail, remove_test_data):
    assert [*create_test_thumbnail.__dict__] == ['_state', 'id', 'image_id', 'url', 'height']
