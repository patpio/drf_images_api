from uuid import UUID

import pytest

from expiring_links.models import ExpiringLink


@pytest.mark.models
def test_expiring_link_creation(db, create_test_expiring_link):
    assert isinstance(create_test_expiring_link, ExpiringLink)
    assert create_test_expiring_link.url == 'http://test_link.com'
    assert isinstance(create_test_expiring_link.token, UUID)
    assert create_test_expiring_link.duration == 350
    assert create_test_expiring_link.__str__() == 'http://test_link.com'


@pytest.mark.models
def test_expiring_link_fields(db, create_test_expiring_link):
    assert [*create_test_expiring_link.__dict__] == ['_state', 'id', 'url', 'token', 'created_at', 'duration']
