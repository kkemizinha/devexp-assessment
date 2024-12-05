import unittest
from unittest.mock import patch
import json
import hmac
import hashlib
from server.webhook_server import app

def verify_signature(message: str, provided_signature: str, secret: str) -> bool:
    """
    Verifies the HMAC SHA256 signature of a webhook message.

    :param message: The raw request body (exactly as received from the webhook).
    :param provided_signature: The signature provided in the `Authorization` header.
    :param secret: The shared secret used to sign the webhook messages.
    :return: True if the signature is valid, False otherwise.
    """
    if not isinstance(message, str) or not isinstance(provided_signature, str) or not isinstance(secret, str):
        raise ValueError("Parameters 'message', 'signature', and 'secret' must all be strings.")

    calculated_signature = hmac.new(secret.encode(), message.encode(), hashlib.sha256).hexdigest()
    return hmac.compare_digest(calculated_signature, provided_signature)

class TestWebhookHandler(unittest.TestCase):
    def setUp(self):
        """
        Set up the Flask test client for the webhook handler.
        """
        self.client = app.test_client()
        self.client.testing = True
    @patch("sdk.utils.signature.verify_signature")
    def test_handle_webhook_expects_invalid_signature(self, mock_verify_signature):
        """
        Test handling a webhook with an invalid signature.
        """
        # Mock the verification to return False
        mock_verify_signature.return_value = False

        # Sample payload
        payload = {"event": "test_event", "data": "sample_data"}
        headers = {
            "Authorization": "Signature invalid_signature"
        }

        response = self.client.post(
            "/webhooks",
            data=json.dumps(payload),
            content_type="application/json",
            headers=headers
        )

        # Assertions
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.get_json(), {"error": "Invalid signature"})

    def test_handle_webhook_expects_missing_authorization_header(self):
        """
        Test handling a webhook request with a missing Authorization header.
        """
        # Sample payload
        payload = {"event": "test_event", "data": "sample_data"}

        response = self.client.post(
            "/webhooks",
            data=json.dumps(payload),
            content_type="application/json"
        )

        # Assertions
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"error": "Missing Authorization header"})

if __name__ == "__main__":
    unittest.main()
