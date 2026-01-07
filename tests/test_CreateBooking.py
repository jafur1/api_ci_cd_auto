import pytest
import allure

from tests.conftest import create_item
from tests.utils.endpoints import Endpoints
from tests.utils.validators import Assert
from tests.utils.models import BookingIdsResponse, Booking, BookingAnswer


@allure.epic("API Тесты")
@allure.feature("Работа с бронью")
class TestBooking:
    @pytest.mark.smoke()
    @pytest.mark.api()
    def test_get_booking(self, api_client):
        with allure.step("Отправить GET запрос для получения списка бронирований"):
            response = api_client.get(endpoint=Endpoints.BOOKING)
        with allure.step("Проверить статус код ответа"):
            Assert.status_code(response, 200)
        with allure.step("Получить и проверить структуру JSON ответа"):
            response_json = response.json
            bookings = BookingIdsResponse(root=response_json)
        with allure.step("Проверить корректность всех ID бронирований"):
            for booking in bookings.root:
                assert booking.bookingid > 0

    @pytest.mark.smoke()
    @pytest.mark.api()
    def test_create_and_delete_booking(self, api_client, item_data, delete_item):
        with allure.step('Отправить POST запрос для создания нового бронирования'):
            response = api_client.post(endpoint=f"{Endpoints.BOOKING}", json=item_data)
        with allure.step("Проверить статус код ответа"):
            Assert.status_code(response, 200)
        with allure.step("Получить и проверить структуру JSON ответа"):
            bookings = BookingAnswer(**response.json)
            assert bookings.booking.firstname == "Jim"
            assert bookings.booking.lastname == "Brown"
        with allure.step('Удалить новую запись после теста'):
            id_item = bookings.bookingid
            delete_item(id_item)

    @pytest.mark.smoke()
    @pytest.mark.api()
    def test_get_booking_by_id(self, api_client,create_item):
        with allure.step("Отправить GET запрос для получения списка бронирований"):
            response = api_client.get(endpoint=f"{Endpoints.BOOKING}/{create_item}")
        with allure.step("Проверить статус код ответа"):
            Assert.status_code(response, 200)
        with allure.step("Получить и проверить структуру JSON ответа"):
            bookings = Booking(**response.json)
            assert bookings.firstname == "Jim"
            assert bookings.lastname == "Brown"