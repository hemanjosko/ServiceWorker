
# Example base URL
from ServiceWorker.serviceworker.serviceworker.src.basewrapper import BaseRequestsWrapper


api_client = BaseRequestsWrapper(base_url="https://api.example.com", headers={"Authorization": "Bearer token"})

# Perform a GET request
response = api_client.get("some/endpoint", params={"query": "example"})
print(response)

# Perform a POST request
response = api_client.post("some/endpoint", json={"key": "value"})
print(response)

# Upload a file
response = api_client.upload_file("upload/endpoint", "path/to/file.txt")
print(response)
