import requests
from requests.exceptions import RequestException
from .authentication import Authentication


class PartneroAPIException(Exception):
    """Custom exception for Partnero SDK errors."""
    def __init__(self, status_code, message):
        super().__init__(f"API Error {status_code}: {message}")
        self.status_code = status_code
        self.message = message


class BaseAPI:
    def __init__(self, base_url: str = "https://api.partnero.com/v1/"):
        self.auth = Authentication()
        self.base_url = base_url
        self.session = requests.Session()  # Use session for connection pooling

    def send_request(self, method: str, endpoint: str, data=None, params=None) -> dict:
        url = f"{self.base_url}{endpoint}"
        headers = self.auth.get_headers()
        try:
            response = self.session.request(method, url, headers=headers, json=data, params=params)
            return self.handle_api_response(response)
        except RequestException as e:
            raise PartneroAPIException(0, f"Network-related error occurred: {str(e)}")

    def handle_api_response(self, response: requests.Response) -> dict:
        if not response.ok:
            error_message = self.parse_error_response(response)
            raise PartneroAPIException(response.status_code, error_message)
        return self.parse_json_response(response)

    @staticmethod
    def parse_error_response(response: requests.Response) -> str:
        try:
            error_details = response.json()
            return error_details.get('message', 'An unknown error occurred')
        except ValueError:
            return response.text

    @staticmethod
    def parse_json_response(response: requests.Response) -> dict:
        try:
            return response.json()
        except ValueError:
            raise PartneroAPIException(0, "Failed to decode JSON response")
