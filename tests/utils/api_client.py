import os
from enum import Enum
from dataclasses import dataclass
from typing import Optional, Dict, Any, Union
import json
import requests

class HTTPMethod(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"

@dataclass
class ApiResponse:
    status_code: int
    headers: dict[str, str]
    body: Union[Dict[str, Any], str, bytes]
    elapsed: float
    request_url: str
    request_method: str

    @property
    def json(self) -> dict:
        if isinstance(self.body, dict):
            return self.body
        try:
            return json.loads(self.body) if self.body else {}
        except (json.JSONDecodeError, TypeError):
            return {}

    @property
    def text(self) -> str:
        if isinstance(self.body, str):
            return self.body
        return str(self.body)

    def is_success(self) -> bool:
        return 200 <= self.status_code < 300

    def assert_status_code(self, expected_code: int):
        assert self.status_code == expected_code,\
            f"Ожидалося статус код {expected_code}, был получент {self.status_code}"

class ApiClient:
    def __init__(self, base_url: str, default_headers: Optional[Dict[str, str]] = None, timeout: int = 30):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()

        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        if default_headers:
            headers.update(default_headers)
        self.session.headers.update(headers)

    def _build_url(self, endpoint: str) -> str:
        return f"{self.base_url}/{endpoint.lstrip('/')}"

    def request(self, method: Union[str, HTTPMethod], endpoint: str, **kwargs) -> ApiResponse:
        url = self._build_url(endpoint)
        if isinstance(method, HTTPMethod):
            method = method.value
        timeout = kwargs.pop('timeout', self.timeout)
        response = self.session.request(
            method=method,
            url=url,
            timeout=timeout,
            **kwargs
        )
        try:
            if response.headers.get('Content-Type', '').startswith('application/json'):
                body = response.json() if response.content else {}
            else:
                body = response.text
        except ValueError:
            body = response.text
        return ApiResponse(
            status_code=response.status_code,
            headers=dict(response.headers),
            body=body,
            elapsed=response.elapsed.total_seconds(),
            request_url=str(response.request.url),
            request_method=response.request.method
        )
    def get(self, endpoint: str,params: Optional[Dict] = None, **kwargs):
        return self.request('get', endpoint, params=params, **kwargs)

    def post(self, endpoint: str,data: Optional[Dict] = None, params: Optional[Dict] = None,
             json: Optional[Dict] = None, **kwargs):
        return self.request('post', endpoint,data=data, json=json, params=params, **kwargs)

    def patch(self,endpoint: str, data: Optional[Dict]= None, json: Optional[Dict] = None, **kwargs):
        return self.request('patch', endpoint, data=data, json=json, **kwargs)

    def put(self,endpoint: str,data: Optional[Dict] = None, json: Optional[Dict] = None, **kwargs):
        return self.request('put', endpoint, data=data, json=json, **kwargs)

    def delete(self,endpoint: str,data: Optional[Dict] = None, json: Optional[Dict] = None, **kwargs):
        return self.request('delete', endpoint, data=data, json=json, **kwargs)

    def set_auth_token(self,token: str):
        self.session.headers['Authorization'] = f'Bearer {token}'

def get_api_client(base_url: Optional[str] = None,
                    default_headers: Optional[dict[str, str]] = None,
                    timeout: Optional[int] = None,
                    auth: Optional[tuple] = None,
                    verify_ssl: bool = True ) -> ApiClient:
    if base_url is None:
        base_url = os.environ.get("CI_API_URL", 'https://restful-booker.herokuapp.com')
    client = ApiClient(base_url, default_headers)
    if auth is not None:
        client.session.auth = auth
    if timeout is None:
        client.session.timeout = timeout
    client.session.verify = verify_ssl
    return client