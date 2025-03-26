import pytest
from rest_framework.test import APIClient

pytest_plugins = [
    'tests.fixtures.fixture_data',
]


@pytest.fixture
def api_client():
    """Фикстура для тестирования API."""
    return APIClient()
