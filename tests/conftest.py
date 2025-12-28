import os
import pytest
from utils.api_client import ApiClient, get_api_client

@pytest.fixture
def api_client() -> ApiClient:
    return get_api_client(
        base_url=os.environ.get("CI_API_URL", "https://restful-booker.herokuapp.com"),
        default_headers={'Authorization': 'Bearer test-token'},
        verify_ssl=False,
        timeout=10
    )

@pytest.fixture
def unauthenticated_api_client() -> ApiClient:
    # клиент без токена
    return get_api_client(
        base_url=os.environ.get("CI_API_URL"),
        verify_ssl=False,
        timeout=10
    )

@pytest.fixture
def test_user_data() -> dict:
    #данные пользователя для токена
    return {
        "email": "test@example.com",
        "password": "TestPass123!"
    }


