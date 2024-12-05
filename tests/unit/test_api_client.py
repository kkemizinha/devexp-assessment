import unittest
from unittest.mock import patch, Mock
from sdk.api_client import APIClient

class TestAPIClient(unittest.TestCase):
    def setUp(self):
        """
        Set up a test instance of APIClient.
        """
        self.client = APIClient(config_path="tests/config_test/test_config.yaml")

    @patch("sdk.api_client.Config")
    def test_api_client_init_expects_correct_config_values(self, MockConfig):
        """
        Test if APIClient initializes with proper config values.
        """
        MockConfig.return_value.api_key = "test_api_key"
        MockConfig.return_value.base_url = "https://api.test.com"
        MockConfig.return_value.timeout = 30

        client = APIClient("tests/config_test/test_config.yaml")
        self.assertEqual(client.api_key, "test_api_key")
        self.assertEqual(client.base_url, "https://api.test.com")
        self.assertEqual(client.timeout, 30)

    def test_get_headers_expects_correct_authorization_header(self):
        """
        Test if headers are generated correctly.
        """
        expected_headers = {
            "Authorization": "Bearer test_api_key",
            "Content-Type": "application/json"
        }
        self.client.api_key = "test_api_key"
        self.assertEqual(self.client._get_headers(), expected_headers)

    @patch("sdk.api_client.requests.request")
    def test_get_request_expects_successful_response(self, mock_request):
        """
        Test a successful GET request.
        """
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"key": "value"}
        mock_request.return_value = mock_response

        response = self.client.request("GET", "test_endpoint")
        self.assertEqual(response, {"key": "value"})
        mock_request.assert_called_once_with(
            "GET",
            f"{self.client.base_url}/test_endpoint",
            headers=self.client._get_headers(),
            params=None,
            json=None,
            timeout=self.client.timeout
        )

    @patch("sdk.api_client.requests.request")
    def test_delete_request_expects_successful_response(self, mock_request):
        """
        Test a successful DELETE request with 204 response (No response)
        """
        mock_response = Mock()
        mock_response.status_code = 204
        mock_request.return_value = mock_response

        response = self.client.request("DELETE", "test_endpoint")
        self.assertIsNone(response)
        mock_request.assert_called_once_with(
            "DELETE",
            f"{self.client.base_url}/test_endpoint",
            headers=self.client._get_headers(),
            params=None,
            json=None,
            timeout=self.client.timeout
        )

if __name__ == "__main__":
    unittest.main()
