import os
import pytest
import requests

from utils.api_client import ApiClient, get_api_client

@pytest.fixture(scope="session")
def base_url() -> str:
    return os.environ.get("CI_API_URL", "https://restful-booker.herokuapp.com")

@pytest.fixture
def auth_token(test_user_data,base_url):
    response = requests.post(
        f"{base_url}/auth",
        json=test_user_data
    )
    return response.json()["token"]

@pytest.fixture
def client(base_url) -> ApiClient: # клиент без токена в хедере
    return get_api_client(
        base_url=base_url,
        verify_ssl=False,
        timeout=10
    )

@pytest.fixture
def test_user_data() -> dict:
    return {
        "username": os.environ.get("TEST_USERNAME", "admin"),
        "password": os.environ.get("TEST_PASSWORD", "password123")
    }

@pytest.fixture
def api_client(client, auth_token) -> ApiClient: # клиент с токеном в хедер
    client.set_auth_token(auth_token)
    return client


