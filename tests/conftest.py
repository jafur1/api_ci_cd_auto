import os
import random

import allure
import pytest
import requests

from tests.utils.api_client import ApiClient, get_api_client
from tests.utils.endpoints import Endpoints


@pytest.fixture(scope="session")
def base_url() -> str:
    return os.environ.get("CI_API_URL", "https://restful-booker.herokuapp.com")

@pytest.fixture
def auth_token(test_user_data,base_url):
    response = requests.post(
        f"{base_url}{Endpoints.TOKEN}",
        json=test_user_data
    )
    return response.json()["token"]

@pytest.fixture
def client(base_url) -> ApiClient: # клиент без токена в хедере
    return get_api_client(
        base_url=base_url,
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

@pytest.fixture
def item_data():
    return {
        "firstname": "Jim",
        "lastname": "Brown",
        "totalprice": random.uniform(10,1000),
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2018-01-01",
            "checkout": "2019-01-01"
        },
        "additionalneeds": "Breakfast"
    }

@pytest.fixture
def delete_item(base_url):
    with allure.step('Отправить DELETE по id'):
        def _delete(booking_id):
            with allure.step(f'Удалить бронирование ID: {booking_id}'):
                response = requests.delete(
                    f"{base_url}{Endpoints.BOOKING}/{booking_id}"
                )
                return response

        return _delete

@pytest.fixture
def create_item(base_url,item_data,delete_item):
    with allure.step('Создать новое бронирование'):
        response = requests.post(
            f"{base_url}{Endpoints.BOOKING}",
            json=item_data
        )
        assert response.status_code == 200, f"Не удалось создать бронирование: {response.status_code}"
        booking_id = response.json()["bookingid"]
        allure.attach(f"Booking ID: {booking_id}", name="Созданное бронирование")
        yield booking_id
        delete_item(booking_id)