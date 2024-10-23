# requests_http_client.py

import requests
from pathlib import Path
from typing import Optional, Union, Dict, Any
from base_http_client import BaseHttpClient  # Import the abstract class


class RequestsHttpClient(BaseHttpClient):
    """
    Concrete implementation of BaseHttpClient using the 'requests' library.
    """

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> Union[Dict[str, Any], str]:
        """
        Implementation of GET request using requests.
        """
        url = self._build_url(endpoint)
        response = requests.get(
            url,
            params=params,
            headers=headers or self.headers,
            timeout=self.timeout
        )
        return self._handle_response(response)

    def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None, json: Optional[Dict[str, Any]] = None,
             files: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> Union[Dict[str, Any], str]:
        """
        Implementation of POST request using requests.
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

    def upload_file(self, endpoint: str, file_path: Union[str, Path], headers: Optional[Dict[str, str]] = None) -> Union[Dict[str, Any], str]:
        """
        Implementation of file upload using POST with requests.
        """
        file_path = Path(file_path)  # Ensure file_path is a Path object

        if not file_path.exists() or not file_path.is_file():
            raise FileNotFoundError(f"File '{file_path}' does not exist or is not a file")

        with file_path.open('rb') as file:
            files = {'file': file}
            return self.post(endpoint, files=files, headers=headers)