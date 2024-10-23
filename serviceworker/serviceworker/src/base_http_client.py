# base_http_client.py

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional, Union, Dict, Any


class BaseHttpClient(ABC):
    """
    Abstract base class for an HTTP client.
    """

    def __init__(self, base_url: str, headers: Optional[Dict[str, str]] = None, timeout: int = 10) -> None:
        """
        Initialize the HTTP client with a base URL, headers, and timeout.
        """
        self.base_url = base_url
        self.headers = headers if headers else {}
        self.timeout = timeout

    @abstractmethod
    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> Union[Dict[str, Any], str]:
        """
        Abstract method for sending GET requests.
        """
        pass

    @abstractmethod
    def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None, json: Optional[Dict[str, Any]] = None,
             files: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> Union[Dict[str, Any], str]:
        """
        Abstract method for sending POST requests.
        """
        pass

    @abstractmethod
    def upload_file(self, endpoint: str, file_path: Union[str, Path], headers: Optional[Dict[str, str]] = None) -> Union[Dict[str, Any], str]:
        """
        Abstract method for uploading files via POST requests.
        """
        pass

    def _build_url(self, endpoint: str) -> str:
        """
        Helper method to build a full URL from an endpoint.
        """
        return f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"

    def _handle_response(self, response) -> Union[Dict[str, Any], str]:
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
        except Exception as err:
            raise SystemExit(f"An error occurred: {err}")
