import pytest 

from categories.models import Category

@pytest.fixture
def create_category():
    def _create_category(name, description):
        return Category.objects.create(name=name, description=description)
    return _create_category
