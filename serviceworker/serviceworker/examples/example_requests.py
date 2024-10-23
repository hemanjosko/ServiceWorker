from serviceworker.src.base_http_client import BaseHttpClient
from serviceworker.src.request_http_client import RequestsHttpClient


if __name__ == "__main__":
    # Initialize the concrete implementation of the HTTP client
    api_client: BaseHttpClient = RequestsHttpClient(
        base_url="https://api.example.com",
        headers={"Authorization": "Bearer token"}
    )

    # Perform a GET request through the base class interface
    response = api_client.get("some/endpoint", params={"query": "example"})
    print(response)

    # Perform a POST request through the base class interface
    response = api_client.post("some/endpoint", json={"key": "value"})
    print(response)

    # Upload a file through the base class interface
    file_path = "path/to/file.txt"
    response = api_client.upload_file("upload/endpoint", file_path)
    print(response)
