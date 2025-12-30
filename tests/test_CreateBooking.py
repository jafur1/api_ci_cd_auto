import pytest
import allure

from tests.utils.endpoints import Endpoints
from utils.validators import Assert
from utils.models import BookingIdsResponse

@allure.epic("API Тесты")
@allure.feature("Получение бронь")
class TestCreateBooking:
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

