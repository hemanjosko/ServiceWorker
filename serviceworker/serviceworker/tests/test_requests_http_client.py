import pytest
from unittest.mock import patch, Mock
from serviceworker.src.request_http_client import RequestsHttpClient

@pytest.fixture
def http_client():
    """Fixture for creating a RequestsHttpClient instance."""
    return RequestsHttpClient(base_url="https://api.example.com")

def test_get_success(http_client):
    """Test successful GET request."""
    with patch("my_package.requests.get") as mock_get:
        # Mock the response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"key": "value"}
        mock_get.return_value = mock_response

        response = http_client.get("some/endpoint", params={"query": "example"})
        
        # Assertions
        assert response == {"key": "value"}
        mock_get.assert_called_once_with(
            "https://api.example.com/some/endpoint",
            params={"query": "example"},
            headers={},
            timeout=http_client.timeout
        )

def test_get_failure(http_client):
    """Test failed GET request."""
    with patch("my_package.requests.get") as mock_get:
        # Mock a failed response
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.text = "Not Found"
        mock_get.return_value = mock_response

        response = http_client.get("some/endpoint")
        
        # Assertions
        assert response == "Not Found"
        mock_get.assert_called_once_with(
            "https://api.example.com/some/endpoint",
            params=None,
            headers={},
            timeout=http_client.timeout
        )

def test_post_success(http_client):
    """Test successful POST request."""
    with patch("my_package.requests.post") as mock_post:
        # Mock the response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"result": "success"}
        mock_post.return_value = mock_response

        response = http_client.post("some/endpoint", json={"key": "value"})
        
        # Assertions
        assert response == {"result": "success"}
        mock_post.assert_called_once_with(
            "https://api.example.com/some/endpoint",
            json={"key": "value"},
            headers={},
            timeout=http_client.timeout
        )

def test_upload_file_success(http_client):
    """Test successful file upload."""
    with patch("my_package.requests.post") as mock_post, patch("pathlib.Path.open", new_callable=Mock) as mock_open:
        # Mock the response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "uploaded"}
        mock_post.return_value = mock_response
        
        # Mock the file context manager
        mock_open.return_value.__enter__.return_value = Mock()
        
        response = http_client.upload_file("upload/endpoint", "path/to/file.txt")
        
        # Assertions
        assert response == {"status": "uploaded"}
        mock_post.assert_called_once_with(
            "https://api.example.com/upload/endpoint",
            files={'file': mock_open.return_value.__enter__.return_value},
            headers={},
            timeout=http_client.timeout
        )

def test_upload_file_not_found(http_client):
    """Test file upload with file not found error."""
    with patch("my_package.requests.post") as mock_post:
        # Raise FileNotFoundError when trying to open the file
        with pytest.raises(FileNotFoundError):
            http_client.upload_file("upload/endpoint", "path/to/nonexistent_file.txt")