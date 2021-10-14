import pytest
from rest_framework import status
from rest_framework.test import force_authenticate

from images.views import ImageViewSet


@pytest.mark.views
def test_user_can_see_own_image(db, api_rf, create_test_user, create_test_image, remove_test_data):
    view = ImageViewSet.as_view({'get': 'list'})
    user = create_test_user

    request = api_rf.get('/api/v1/images/')
    force_authenticate(request, user)
    response = view(request)

    assert response.status_code == status.HTTP_200_OK
    assert response.data[0].get('id') == create_test_image.pk
    assert response.data[0].get('name') == 'test_file.jpg'
    assert response.data[0].get('author') == create_test_user.pk


@pytest.mark.views
def test_user_can_see_own_image_with_link(db, api_rf, create_test_user, create_test_image, remove_test_data):
    view = ImageViewSet.as_view({'get': 'list'})
    user = create_test_user
    user.tier.link_flag = True

    request = api_rf.get('/api/v1/images/')
    force_authenticate(request, user)
    response = view(request)

    assert response.status_code == status.HTTP_200_OK
    assert response.data[0].get('id') == create_test_image.pk
    assert response.data[0].get('url') == "http://testserver/media/images/test_file.jpg"
    assert response.data[0].get('name') == 'test_file.jpg'
    assert response.data[0].get('author') == create_test_user.pk
