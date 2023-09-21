
import pytest
from orders.models import Order

@pytest.fixture
def create_order():
    def _create_order(user):
        return Order.objects.create(user=user)
    return _create_order