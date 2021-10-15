import pytest
from rest_framework import status
from rest_framework.test import force_authenticate

from images.views import ThumbnailViewSet


@pytest.mark.views
def test_user_can_make_thumbnail(db, api_rf, create_test_user, create_test_image, create_test_thumbnail,
                                 remove_test_data):
    view = ThumbnailViewSet.as_view({'post': 'create'})
    user = create_test_user

    request = api_rf.post(
        '/api/v1/thumbnails/',
        {
            'image_id': create_test_image.pk,
            'heights': [200]
        },
        format='json'
    )
    force_authenticate(request, user)
    response = view(request)

    assert response.status_code == status.HTTP_200_OK
    assert response.data.get('links')[0] == 'http://testserver/media/resized_images/test_resized_file.jpg'


@pytest.mark.views
def test_user_cannot_make_thumbnail_with_wrong_height(db, api_rf, create_test_user, create_test_image,
                                                      create_test_thumbnail, remove_test_data):
    view = ThumbnailViewSet.as_view({'post': 'create'})
    user = create_test_user

    request = api_rf.post(
        '/api/v1/thumbnails/',
        {
            'image_id': create_test_image.pk,
            'heights': [100]
        },
        format='json'
    )
    force_authenticate(request, user)
    response = view(request)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert set(response.data) == {'heights'}
    assert response.data.get('heights')[0] == 'Chosen height (100 px) is not available in your tier (test tier).'


@pytest.mark.views
def test_user_can_get_list_of_thumbnails_for_given_image(db, api_rf, create_test_user, create_test_image,
                                                         create_test_thumbnail,
                                                         remove_test_data):
    view = ThumbnailViewSet.as_view({'get': 'retrieve'})
    user = create_test_user

    pk = create_test_image.pk

    request = api_rf.get(f'/api/v1/thumbnails/{pk}')
    force_authenticate(request, user)
    response = view(request, pk)

    assert response.status_code == status.HTTP_200_OK
    assert '/'.join(response.data[0].get('url').split('/')[-2:]) == create_test_thumbnail.url.name
    assert response.data[0].get('height') == create_test_thumbnail.height
    assert response.data[0].get('image') == create_test_image.pk


@pytest.mark.views
def test_user_cannot_get_list_of_thumbnails_for_wrong_image(db, api_rf, create_test_user, create_test_image,
                                                            remove_test_data):
    view = ThumbnailViewSet.as_view({'get': 'retrieve'})
    user = create_test_user

    pk = create_test_image.pk + 1

    request = api_rf.get(f'/api/v1/thumbnails/{pk}')
    force_authenticate(request, user)
    response = view(request, pk)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'Image with given id does not exist.' in response.data
