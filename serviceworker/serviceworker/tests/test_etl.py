import pytest
from unittest.mock import patch, Mock
from serviceworker.src.etl import ETLProcess

@pytest.fixture
def etl_process():
    """Fixture for creating an ETLProcess instance."""
    return ETLProcess(source_url="https://api.example.com", destination_url="https://api.destination.com")

def test_extract(etl_process):
    """Test the extract method."""
    with patch("my_package.requests.get") as mock_get:
        mock_response = Mock()
        mock_response.json.return_value = {"items": [{"id": 1, "name": "Item1", "value": 10}]}
        mock_get.return_value = mock_response

        data = etl_process.extract()
        assert data == {"items": [{"id": 1, "name": "Item1", "value": 10}]}
        mock_get.assert_called_once()

def test_transform(etl_process):
    """Test the transform method."""
    input_data = {"items": [{"id": 1, "name": "Item1", "value": 10}]}
    expected_output = {1: {"name": "ITEM1", "value": 20}}
    transformed_data = etl_process.transform(input_data)
    assert transformed_data == expected_output

def test_load(etl_process):
    """Test the load method."""
    with patch("my_package.requests.post") as mock_post:
        mock_response = Mock()
        mock_response.json.return_value = {"status": "success"}
        mock_post.return_value = mock_response

        data_to_load = {1: {"name": "ITEM1", "value": 20}}
        response = etl_process.load(data_to_load)
        assert response == {"status": "success"}
        mock_post.assert_called_once_with("https://api.destination.com/destination/endpoint", json=data_to_load)

def test_run(etl_process):
    """Test the entire ETL process."""
    with patch.object(etl_process, 'extract') as mock_extract, \
         patch.object(etl_process, 'transform') as mock_transform, \
         patch.object(etl_process, 'load') as mock_load:

        mock_extract.return_value = {"items": [{"id": 1, "name": "Item1", "value": 10}]}
        mock_transform.return_value = {1: {"name": "ITEM1", "value": 20}}
        mock_load.return_value = {"status": "success"}

        response = etl_process.run()
        assert response == {"status": "success"}
        mock_extract.assert_called_once()
        mock_transform.assert_called_once_with(mock_extract.return_value)
        mock_load.assert_called_once_with(mock_transform.return_value)
