import requests
import os

class BaseRequestsWrapper:
    def __init__(self, base_url: str, headers: dict = None, timeout: int = 10):
        """
        Initialize the BaseRequestsWrapper.

        :param base_url: Base URL for the API.
        :param headers: Default headers to be used in every request.
        :param timeout: Default timeout for requests (in seconds).
        """
        self.base_url = base_url
        self.headers = headers if headers else {}
        self.timeout = timeout

    def _build_url(self, endpoint: str) -> str:
        """Helper method to build a full URL from an endpoint."""
        return os.path.join(self.base_url, endpoint)

    def get(self, endpoint: str, params: dict = None, headers: dict = None):
        """
        Send a GET request.

        :param endpoint: API endpoint to send the request to.
        :param params: URL parameters to include in the GET request.
        :param headers: Optional headers to include.
        :return: Response object.
        """
        url = self._build_url(endpoint)
        response = requests.get(
            url, 
            params=params, 
            headers=headers or self.headers, 
            timeout=self.timeout
        )
        return self._handle_response(response)

    def post(self, endpoint: str, data: dict = None, json: dict = None, files: dict = None, headers: dict = None):
        """
        Send a POST request.

        :param endpoint: API endpoint to send the request to.
        :param data: Form data to include in the POST request.
        :param json: JSON data to include in the POST request.
        :param files: Files to be uploaded.
        :param headers: Optional headers to include.
        :return: Response object.
        """
        url = self._build_url(endpoint)
        response = requests.post(
            url,
            data=data,
            json=json,
            files=files,
            headers=headers or self.headers,
            timeout=self.timeout
        )
        return self._handle_response(response)

    def upload_file(self, endpoint: str, file_path: str, headers: dict = None):
        """
        Upload a file via POST request.

        :param endpoint: API endpoint to send the request to.
        :param file_path: Path to the file to be uploaded.
        :param headers: Optional headers to include.
        :return: Response object.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File '{file_path}' does not exist")

        with open(file_path, 'rb') as f:
            files = {'file': f}
            return self.post(endpoint, files=files, headers=headers)

    def _handle_response(self, response):
        """
        Handle the response from requests.

        :param response: The response object.
        :return: JSON response or raise an exception if the request failed.
        """
        try:
            response.raise_for_status()
            if response.headers.get('Content-Type', '').startswith('application/json'):
                return response.json()  # Return JSON if the response is in JSON format
            return response.text  # Otherwise, return text content
        except requests.exceptions.HTTPError as err:
            raise SystemExit(f"HTTP error occurred: {err}")
        except Exception as err:
            raise SystemExit(f"An error occurred: {err}")