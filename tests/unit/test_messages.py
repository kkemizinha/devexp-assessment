import unittest
from unittest.mock import Mock
from sdk.resources.messages import Messages
from sdk.api_client import APIClient

class TestMessages(unittest.TestCase):
    def setUp(self):
        """
        Set up a mock client and Messages instance for testing.
        """
        self.mock_client = Mock(spec=APIClient)
        self.messages = Messages(client=self.mock_client, webhook_secret="test_secret")

    def test_send_message_expects_successful_delivery(self):
        """
        Test sending a message successfully.
        """
        self.mock_client.request.return_value = {
            "to": {"id": "d1234567-8abc-4def-9012-3456789abcdef"},
            "from": "+14155552672",
            "content": "Hello!",
            "id": "456",
            "status": "delivered",
            "createdAt": "2024-01-01T12:00:00Z",
            "deliveredAt": "2024-01-01T12:05:00Z"
        }

        response = self.messages.send_message(
            recipient_id="d1234567-8abc-4def-9012-3456789abcdef",
            content="Hello!",
            sender_phone="+14155552672"
        )
        self.assertEqual(response["status"], "delivered")
        self.mock_client.request.assert_called_once_with(
            "POST", "messages", json={
                "to":
                    {"id": "d1234567-8abc-4def-9012-3456789abcdef"},
                "from": "+14155552672",
                "content": "Hello!"
            }
        )

    def test_send_message_expects_exception_for_missing_parameters(self):
        """
        Test if send_message raises ValueError for missing parameters.
        """
        with self.assertRaises(ValueError):
            self.messages.send_message(recipient_id="", content="Hello!", sender_phone="+14155552672")
        with self.assertRaises(ValueError):
            self.messages.send_message(recipient_id="123", content="", sender_phone="+14155552672")
        with self.assertRaises(ValueError):
            self.messages.send_message(recipient_id="123", content="Hello!", sender_phone="")

    def test_list_messages_expects_correct_pagination(self):
        """
        Test listing messages with pagination.
        """
        self.mock_client.request.return_value = {
            "messages": [{"id": "123", "content": "Hello!"}],
            "pagination": {"page": 1, "limit": 10, "total": 100}
        }

        response = self.messages.list_messages(page=1, limit=10)
        self.assertEqual(response["messages"][0]["content"], "Hello!")
        self.mock_client.request.assert_called_once_with(
            "GET", "messages", params={"page": 1, "limit": 10}
        )

    def test_get_message_expects_successful_retrieval(self):
        """
        Test retrieving a message by ID.
        """
        self.mock_client.request.return_value = {
            "id": "123", "content": "Hello!", "from": "+14155552672"
        }

        response = self.messages.get_message(message_id="123")
        self.assertEqual(response["content"], "Hello!")
        self.mock_client.request.assert_called_once_with("GET", "messages/123")

    def test_get_message_expects_exception_for_invalid_id(self):
        """
        Test if get_message raises ValueError for an invalid message ID.
        """
        with self.assertRaises(ValueError):
            self.messages.get_message(message_id=None)

if __name__ == "__main__":
    unittest.main()
