import pytest

from images.serializers import ThumbnailGeneratorSerializer


@pytest.mark.serializers
def test_fields(db, create_test_thumbnail_serializer_data):
    assert list(create_test_thumbnail_serializer_data.keys()) == ['image_id', 'heights']


@pytest.mark.serializers
def test_valid_serializer(db, create_test_thumbnail_serializer_data, create_test_image, create_test_user,
                          remove_test_data):
    serializer = ThumbnailGeneratorSerializer(data=create_test_thumbnail_serializer_data,
                                              context={'user': create_test_user})

    assert serializer.is_valid()


@pytest.mark.serializers
def test_wrong_image_id(db, create_test_thumbnail_serializer_data, create_test_image, create_test_user,
                        remove_test_data):
    create_test_thumbnail_serializer_data['image_id'] = create_test_image.pk + 1

    serializer = ThumbnailGeneratorSerializer(data=create_test_thumbnail_serializer_data,
                                              context={'user': create_test_user})

    assert not serializer.is_valid()
    assert set(serializer.errors) == {'image_id'}


@pytest.mark.serializers
def test_wrong_height_data_type(db, create_test_thumbnail_serializer_data, create_test_image, create_test_user,
                                remove_test_data):
    create_test_thumbnail_serializer_data['heights'] = ['not_an_int']

    serializer = ThumbnailGeneratorSerializer(data=create_test_thumbnail_serializer_data,
                                              context={'user': create_test_user})

    assert not serializer.is_valid()
    assert set(serializer.errors) == {'heights'}


@pytest.mark.serializers
def test_height_not_positive(db, create_test_thumbnail_serializer_data, create_test_image, create_test_user,
                             remove_test_data):
    create_test_thumbnail_serializer_data['heights'] = [0]

    serializer = ThumbnailGeneratorSerializer(data=create_test_thumbnail_serializer_data,
                                              context={'user': create_test_user})

    assert not serializer.is_valid()
    assert set(serializer.errors) == {'heights'}


@pytest.mark.serializers
def test_height_not_available(db, create_test_thumbnail_serializer_data, create_test_image, create_test_user,
                              remove_test_data):
    create_test_thumbnail_serializer_data['heights'] = [100]

    serializer = ThumbnailGeneratorSerializer(data=create_test_thumbnail_serializer_data,
                                              context={'user': create_test_user})

    assert not serializer.is_valid()
    assert set(serializer.errors) == {'heights'}
