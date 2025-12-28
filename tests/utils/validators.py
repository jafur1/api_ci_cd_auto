from typing import Dict, Any, List
import jsonschema
from deepdiff import DeepDiff

class ResponseValidator:
    @staticmethod
    def validate_json_schema(response: Dict[str, Any], schema: Dict[str, Any]):
        jsonschema.validate(response, schema)
    @staticmethod
    def compare_objects(actual: Any, expected: Any, exclude: List[str] = None):
        return DeepDiff(actual, expected, exclude=exclude, ignore_order=True,report_repetition=True)
