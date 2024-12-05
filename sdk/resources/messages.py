import hmac
import hashlib
from typing import Any, Dict, Optional


class Messages:
    """
    A class to manage operations related to messages, such as sending, receiving, and validating them.

    This class also supports webhook signature verification to ensure the messages are authentic.
    """

    def __init__(self, client: 'APIClient', webhook_secret: str = None) -> None:
        """
        Initialize the Messages class with the provided API client.

        :param client: An instance of the API client.
        :param webhook_secret: The secret used to verify webhook signatures.
        """
        self.client = client
        self.webhook_secret = webhook_secret

    def generate_signature(self, content: str, secret: Optional[str] = None) -> str:
        """
        Generate HMAC signature for the message payload.

        :param content: The raw payload as a string.
        :param secret: (Optional) The secret key for HMAC signing. If not provided, the webhook secret will be used.
        :return: The HMAC SHA-256 signature as a hexadecimal string.
        :raises ValueError: If no valid secret key is available.
        """
        secret = secret or self.webhook_secret
        if not secret:
            raise ValueError("A valid secret key must be provided for signature generation.")

        hmac_obj = hmac.new(secret.encode('utf-8'), content.encode('utf-8'), hashlib.sha256)
        return hmac_obj.hexdigest()

    def send_message(self, recipient_id: str, content: str, sender_phone: str) -> Dict[str, any]:
        """
        Send a new message to a contact.

        :param recipient_id: The ID of the contact to send the message to.
        :param content: The text content of the message.
        :param sender_phone: The sender's phone number.
        :return: A dictionary representing the response from the API, which includes:
                 - to (dict): Details of the recipient (name, phone, id).
                 - from (str): The sender's phone number.
                 - content (str): The content of the message.
                 - id (str): The ID of the message.
                 - status (str): The current status of the message.
                 - createdAt (str): The timestamp when the message was created.
                 - deliveredAt (str): The timestamp when the message was delivered.
        :raises ValueError: If any of the required parameters are missing.
        """
        if not recipient_id:
            raise ValueError("Parameter 'recipient_id' is required.")
        if not content:
            raise ValueError("Parameter 'content' is required.")
        if not sender_phone:
            raise ValueError("Parameter 'sender' is required.")

        payload = {
            "to": {"id": recipient_id},
            "from": sender_phone,
            "content": content
        }

        response = self.client.request("POST", "messages", json=payload)

        expected_keys = ["to", "from", "content", "id", "status", "createdAt", "deliveredAt"]
        if not all(key in response for key in expected_keys):
            raise RuntimeError("The response from the API is missing expected keys.")

        return response

    def list_messages(self, page: int = 1, limit: int = 100) -> Dict:
        """
        Retrieve a paginated list of sent messages.

        :param page: The page number to fetch (default is 1).
        :param limit: The maximum number of messages per page (default is 100).
        :return: A dictionary containing:
                 - 'messages' (list): A list of messages.
                 - 'pagination' (dict): Pagination details including 'page', 'limit', and 'total'.
        :raises ValueError: If 'page' or 'limit' are not valid.
        """
        if page < 1:
            raise ValueError("Parameter 'page' must be greater than or equal to 1.")
        if limit <= 0:
            raise ValueError("Parameter 'limit' must be greater than 0.")

        params = {
            "page": page,
            "limit": limit
        }
        response = self.client.request("GET", "messages", params=params)
        return response

    def get_message(self, message_id: str) -> Dict:
        """
        Retrieve details of a specific message by its ID.

        :param message_id: The ID of the message to retrieve.
        :return: A dictionary containing the message details.
        :raises ValueError: If 'message_id' is not valid.
        """
        if not isinstance(message_id, str):
            raise ValueError("The 'message_id' must be a non-empty string.")

        response = self.client.request("GET", f"messages/{message_id}")
        return response