import pytest

from tiers.models import Tier, Size


@pytest.fixture(scope='function')
def create_test_tier(create_test_size):
    tier = Tier.objects.create(
        name='test tier',
        expired_link_flag=True
    )
    tier.size.add(create_test_size)
    return tier


@pytest.fixture(scope='function')
def create_test_size():
    size = Size.objects.create(
        height=200
    )
    return size
