import unittest
from unittest.mock import patch,Mock
from sdk.resources.contacts import Contacts


class TestContacts(unittest.TestCase):
    def setUp(self):
        """
        Set up the mock API client and initialize Contacts.
        """
        self.mock_client = Mock()
        self.contacts = Contacts(self.mock_client)

    def test_validate_phone_number_expects_valid_format(self):
        """
        Test validating a valid phone number.
        """
        valid_phone = "+14155552671"
        formatted_phone = self.contacts.validate_phone_number(valid_phone)
        self.assertEqual(formatted_phone, "+14155552671")

    def test_validate_phone_number_expects_exception_for_invalid_phone(self):
        """
        Test validating an invalid phone number.
        """
        invalid_phone = "12345"
        with self.assertRaises(ValueError):
            self.contacts.validate_phone_number(invalid_phone)

    def test_create_contact_expects_value_error_for_missing_name(self):
        """
        Test creating a contact with missing name raises ValueError.
        """
        with self.assertRaises(ValueError):
            self.contacts.create_contact(name="", phone="+14155552671")

    def test_create_contact_expects_value_error_for_missing_phone(self):
        """
        Test creating a contact with missing phone raises ValueError.
        """
        with self.assertRaises(ValueError):
            self.contacts.create_contact(name="John Doe", phone="")

    def test_get_contact_expects_successful_retrieval(self):
        """
        Test retrieving an existing contact successfully.
        """
        contact_id = "b8704130-5be8-4b5f-ba71-8f4da96ef5a8"

        # Mock the response for GET request
        self.mock_client.request.return_value = {
            "id": contact_id,
            "name": "Jane Smith",
            "phone": "+34612345678"
        }

        # Call the get method
        contact = self.contacts.get_contact(contact_id)

        # Verify the request
        self.mock_client.request.assert_called_once_with(
            "GET",
            f"contacts/{contact_id}"
        )

        # Validate the response
        self.assertEqual(contact["id"], contact_id)
        self.assertEqual(contact["name"], "Jane Smith")
        self.assertEqual(contact["phone"], "+34612345678")

    def test_create_contact_expects_successful_creation(self):
        """
        Test creating a new contact successfully.
        """
        # Mock the response for POST request
        self.mock_client.request.return_value = {
            "id": "d1234567-8abc-4def-9012-3456789abcdef",
            "name": "Jane Smith",
            "phone": "+34612345678"
        }

        new_contact_data = {"name": "Jane Smith", "phone": "+34612345678"}

        # Call the create method
        contact = self.contacts.create_contact(name=new_contact_data["name"], phone=new_contact_data["phone"])

        # Verify the request
        self.mock_client.request.assert_called_once_with(
            "POST",
            "contacts",
            json=new_contact_data
        )

        # Validate the response
        self.assertIn("id", contact)
        self.assertEqual(contact["name"], "Jane Smith")
        self.assertEqual(contact["phone"], "+34612345678")

    def test_update_contact_expects_successful_update(self):
        """
        Test updating a contact successfully.
        """
        contact_id = "b8704130-5be8-4b5f-ba71-8f4da96ef5a8"

        # Mock the responses for GET and PATCH requests
        def mock_request(method, endpoint, json=None):
            if method == "GET" and endpoint == f"contacts/{contact_id}":
                return {"id": contact_id, "name": "Jane Smith", "phone": "+1234567890"}
            if method == "PATCH" and endpoint == f"contacts/{contact_id}":
                return {"id": contact_id, "name": "Jane Smith", "phone": "+34612345678"}
            return None

        self.mock_client.request.side_effect = mock_request

        # Fetch the existing contact
        existing_contact = self.contacts.get_contact(contact_id)
        self.assertEqual(existing_contact["id"], contact_id)
        self.assertEqual(existing_contact["name"], "Jane Smith")
        self.assertEqual(existing_contact["phone"], "+1234567890")

        # Update the contact's phone number
        updated_data = {"phone": "+34612345678"}
        updated_contact = self.contacts.update_contact(contact_id, phone=updated_data["phone"])

        # Verify the PATCH request
        self.mock_client.request.assert_any_call(
            "PATCH",
            f"contacts/{contact_id}",
            json=updated_data
        )

        # Validate the updated response
        self.assertEqual(updated_contact["id"], contact_id)
        self.assertEqual(updated_contact["name"], "Jane Smith")
        self.assertEqual(updated_contact["phone"], "+34612345678")


if __name__ == "__main__":
    unittest.main()
