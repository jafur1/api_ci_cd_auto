from typing import Dict, Any, List
import jsonschema
from deepdiff import DeepDiff
import allure

class ResponseValidator:
    @staticmethod
    def validate_json_schema(response: Dict[str, Any], schema: Dict[str, Any]):
        jsonschema.validate(response, schema)
    @staticmethod
    def compare_objects(actual: Any, expected: Any, exclude: List[str] = None):
        return DeepDiff(actual, expected, exclude=exclude, ignore_order=True,report_repetition=True)

class Assert:
    @staticmethod
    @allure.step('Проверка статуса кода')
    def status_code(response, expected_code: int):
        assert response.status_code == expected_code,\
            f"Ожидался код {expected_code}, был получен {response.status_code}"

    @staticmethod
    @allure.step('Проверка скорости выполнения запроса')
    def response_time(response, expected_time: float):
        response_time_actual = response.elapsed
        assert response_time_actual <= expected_time, \
            f'Время выполнения запроса {response_time_actual}с, максимальное время {expected_time}с'
