import datetime
import os

import pytest
from rest_framework import status
from rest_framework.test import force_authenticate
from django.test import override_settings

from expiring_links.views import ExpiringLinkView


@pytest.mark.views
def test_user_can_make_expiring_link(db, api_rf, create_test_user, create_test_image, remove_test_data):
    view = ExpiringLinkView.as_view({'post': 'create'})
    user = create_test_user

    request = api_rf.post(
        '/api/v1/links/',
        {
            'image_id': create_test_image.pk,
            'expiration_time': 350
        },
        format='json'
    )
    force_authenticate(request, user)
    response = view(request)

    assert response.status_code == status.HTTP_200_OK
    assert response.data.get('link').rsplit('/', 1)[0] == 'http://testserver/api/v1/links'


@pytest.mark.views
def test_user_cannot_make_expiring_link_because_of_tier(db, api_rf, create_test_user, create_test_image,
                                                        remove_test_data):
    view = ExpiringLinkView.as_view({'post': 'create'})
    user = create_test_user
    user.tier.expired_link_flag = False

    request = api_rf.post(
        '/api/v1/links/',
        {
            'image_id': create_test_image.pk,
            'expiration_time': 350
        },
        format='json'
    )
    force_authenticate(request, user)
    response = view(request)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert set(response.data) == {'non_field_errors'}
    assert response.data.get('non_field_errors')[0] == 'Your tier have no access for expiring links.'


@pytest.mark.views
@override_settings(MEDIA_URL=(os.environ.get('TEST_DIR').rsplit('/')[-1] + '/media'))
def test_user_can_get_image_with_expiring_link(db, api_rf, create_test_image, create_test_expiring_link,
                                               remove_test_data):
    view = ExpiringLinkView.as_view({'get': 'retrieve'})

    expiring_link = create_test_expiring_link
    expiring_link.url = create_test_image.url
    expiring_link.save()

    token = str(expiring_link.token)

    request = api_rf.get(f'/api/v1/links/{token}.jpg')
    response = view(request, token)

    assert response.status_code == status.HTTP_200_OK
    assert create_test_image.name in response.headers['Content-Disposition']


@pytest.mark.views
@override_settings(MEDIA_URL=(os.environ.get('TEST_DIR').rsplit('/')[-1] + '/media'))
def test_user_cannot_get_image_with_expired_link(db, api_rf, create_test_image, create_test_expiring_link,
                                                 remove_test_data):
    view = ExpiringLinkView.as_view({'get': 'retrieve'})

    expiring_link = create_test_expiring_link
    expiring_link.created_at -= datetime.timedelta(days=1)
    expiring_link.save()

    expiration_date = expiring_link.created_at + datetime.timedelta(seconds=expiring_link.duration)
    token = str(expiring_link.token)

    request = api_rf.get(f'/api/v1/links/{token}.jpg')
    response = view(request, token)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == f'Link is no more available. Expiration date: {expiration_date}.'
