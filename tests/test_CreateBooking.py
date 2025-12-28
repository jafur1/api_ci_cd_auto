import pytest
import allure
from tests.utils.endpoints import Endpoints

@allure.epic("API Tests")
@allure.feature("Create Booking")
class TestCreateBooking:
    @pytest.mark.smoke()
    @pytest.mark.api()
    def test_create_booking(self, api_client, endpoint: Endpoints):
        pass
