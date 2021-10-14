import pytest

from images.serializers import ImageSerializerWithoutOriginalLink


@pytest.mark.serializers
def test_fields(db, create_test_image, remove_test_data):
    serializer = ImageSerializerWithoutOriginalLink(instance=create_test_image)
    serializer_data = serializer.data

    assert list(serializer_data.keys()) == ['id', 'name', 'created_at', 'updated_at', 'author']
