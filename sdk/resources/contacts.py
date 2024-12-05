import phonenumbers
import logging
from typing import Optional, Dict, List, Union

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class Contacts:
    """
    A class to manage operations related to contacts.
    """

    def __init__(self, client, default_region: Optional[str] = None) -> None:
        """
        Initialize the Contacts class with the provided API client.

        :param client: An instance of the API client.
        :param default_region: (Optional) The default region code (e.g., 'US').
        """
        self.client = client
        self.default_region = default_region  # For phone number parsing

    def validate_phone_number(self, phone: str) -> str:
        """
        Validate and format a phone number to E.164 format.

        :param phone: The phone number to validate.
        :return: The phone number formatted in E.164 format.
        :raises ValueError: If the phone number is invalid.
        """
        try:
            parsed_phone = phonenumbers.parse(phone, self.default_region)
            if not phonenumbers.is_valid_number(parsed_phone):
                raise ValueError("Invalid phone number.")
            formatted_phone = phonenumbers.format_number(
                parsed_phone, phonenumbers.PhoneNumberFormat.E164
            )
            return formatted_phone
        except phonenumbers.NumberParseException as e:
            raise ValueError(f"Invalid phone number: {e}")

    def create_contact(self, name: str, phone: str) -> Dict[str, str]:
        """
        Create a new contact.

        :param name: The name of the contact.
        :param phone: The phone number of the contact.
        :return: The response from the API, typically the contact ID and details.
        """
        if not all([name, phone]):
            raise ValueError("Parameters 'name' and 'phone' are required.")
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Parameter 'name' must be a non-empty string.")
        if not isinstance(phone, str) or not phone.strip():
            raise ValueError("Parameter 'phone' must be a non-empty string.")

        # Validate the phone number
        formatted_phone = self.validate_phone_number(phone)

        payload = {
            "name": name,
            "phone": formatted_phone
        }
        logging.debug("Payload for creating contact: %s", payload)

        try:
            response = self.client.request("POST", "contacts", json=payload)
        except Exception as e:
            raise RuntimeError(f"Failed to create contact: {e}")

        return response

    def list_contacts(self, page: int = 1, limit: int = 10) -> Dict[str, Union[List[Dict[str, str]], int]]:
        """
        Retrieve a paginated list of contacts.

        :param page: The page number to fetch (default is 1).
        :param limit: The maximum number of contacts per page (default is 10).
        :return: A dictionary containing the list of contacts and pagination details.
        """
        if page < 1 or limit < 1:
            raise ValueError("Parameters 'page' and 'limit' must be positive integers.")

        params = {
            "page": page,
            "limit": limit
        }
        response = self.client.request("GET", "contacts", params=params)
        return response

    def get_contact(self, contact_id: str) -> Dict[str, str]:
        """
        Retrieve details of a specific contact by its ID.

        :param contact_id: The ID of the contact to retrieve.
        :return: A dictionary containing the contact details.
        """
        if not contact_id:
            raise ValueError("The 'contact_id' is required to fetch contact details.")

        response = self.client.request("GET", f"contacts/{contact_id}")
        return response

    def update_contact(
            self,
            contact_id: str,
            name: Optional[str] = None,
            phone: Optional[str] = None
    ) -> Dict[str, str]:
        """
        Updates a contact's details.

        :param contact_id: ID of the contact to update.
        :param name: New name of the contact.
        :param phone: New phone number of the contact.
        :return: The updated contact details.
        """
        endpoint = f"contacts/{contact_id}"
        payload = {}
        if name:
            payload["name"] = name
        if phone:
            phone = self.validate_phone_number(phone)
            payload["phone"] = phone

        if not payload:
            raise ValueError("No fields provided for update")

        response = self.client.request("PATCH", endpoint, json=payload)
        return response

    def delete_contact(self, contact_id: str) -> Dict[str, Union[str, bool]]:
        """
        Delete a contact by its ID.

        :param contact_id: The ID of the contact to delete.
        :return: The response from the API indicating success or failure.
        """
        if not contact_id:
            raise ValueError("The 'contact_id' is required to delete a contact.")

        response = self.client.request("DELETE", f"contacts/{contact_id}")
        return response
