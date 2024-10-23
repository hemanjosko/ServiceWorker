from typing import Dict, Any
import logging

from serviceworker.src.request_http_client import RequestsHttpClient

class ETLProcess:
    def __init__(self, source_url: str, destination_url: str):
        self.client = RequestsHttpClient(base_url=source_url)
        self.destination_url = destination_url

    def extract(self) -> Dict[str, Any]:
        """Extract data from the source API."""
        try:
            response = self.client.get("data/endpoint")  # Adjust the endpoint as needed
            return response  # Assuming response is already a dict
        except Exception as e:
            logging.error(f"Error during extraction: {e}")
            raise

    def transform(self, data: Dict[str, Any]) -> Dict[int, Dict[str, Any]]:
        """Transform the extracted data."""
        # Example transformation: filter and modify the data
        transformed_data = {}
        for item in data.get("items", []):
            transformed_data[item["id"]] = {
                "name": item["name"].upper(),  # Transform name to uppercase
                "value": item["value"] * 2     # Example transformation
            }
        return transformed_data

    def load(self, data: Dict[int, Dict[str, Any]]) -> Dict[str, Any]:
        """Load the transformed data to the destination API."""
        try:
            response = self.client.post("destination/endpoint", json=data)  # Adjust the endpoint as needed
            return response
        except Exception as e:
            logging.error(f"Error during loading: {e}")
            raise

    def run(self) -> Dict[str, Any]:
        """Run the ETL process."""
        extracted_data = self.extract()
        transformed_data = self.transform(extracted_data)
        load_response = self.load(transformed_data)
        return load_response
