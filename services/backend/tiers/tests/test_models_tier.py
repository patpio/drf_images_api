import pytest

from tiers.models import Tier


@pytest.mark.models
def test_tier_creation(db, create_test_tier, create_test_size):
    assert isinstance(create_test_tier, Tier)
    assert create_test_tier.name == 'test tier'
    assert not create_test_tier.link_flag
    assert create_test_tier.expired_link_flag
    assert create_test_tier.size.get(height=200) == create_test_size
    assert create_test_tier.__str__() == 'test tier'


@pytest.mark.models
def test_tier_fields(db, create_test_tier):
    assert [*create_test_tier.__dict__] == ['_state', 'id', 'name', 'link_flag', 'expired_link_flag']
