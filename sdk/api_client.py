import logging
import requests
from .config import Config

class APIClient:
    def __init__(self, config_path="config.yaml"):
        """
        Initializes the API client using the configuration file.
        :param config_path: Path to the configuration file.
        """
        self.config = Config(config_path)
        self.api_key = self.config.api_key
        self.base_url = self.config.base_url
        self.timeout = self.config.timeout

    def _get_headers(self):
        """
        Prepares the headers for API requests, including the Authorization header.
        """
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"  # Ensure this is included
        }

    def request(self, method, endpoint, params=None, json=None, headers=None):
        """
        Sends an HTTP request to the API and handles responses.
        :param method: HTTP method (GET, POST, PATCH, DELETE).
        :param endpoint: API endpoint (e.g., "contacts").
        :param params: Query parameters.
        :param json: Request body as JSON.
        :return: Decoded JSON response, or None for 204 No Content.
        """
        url = f"{self.base_url}/{endpoint}"
        if not headers:
            headers = self._get_headers()

        try:
            response = requests.request(
                method, url, headers=headers, params=params, json=json, timeout=self.timeout
            )
            logging.debug("Response content: %s", response.text)
            response.raise_for_status()

            if response.status_code == 204:  # Handle successful deletion
                return None

            return response.json()  # Decode JSON for other responses
        except requests.exceptions.RequestException as e:
            logging.error(f"Request to {url} failed: {e}")
            raise
        except requests.exceptions.HTTPError as e:
            logging.error(f"Bad Request for  {url} failed: {e}")
            raise
        except ValueError as e:
            logging.error(f"Failed to decode JSON response from {url}: {e}")
            raise
