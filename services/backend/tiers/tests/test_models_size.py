import pytest

from tiers.models import Size


@pytest.mark.models
def test_size_creation(db, create_test_size):
    assert isinstance(create_test_size, Size)
    assert create_test_size.height == 200
    assert create_test_size.__str__() == '200 px'


@pytest.mark.models
def test_size_fields(db, create_test_size):
    assert [*create_test_size.__dict__] == ['_state', 'id', 'height']
