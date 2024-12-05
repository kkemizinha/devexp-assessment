import unittest
from sdk.resources.contacts import Contacts
from sdk.resources.messages import Messages
from sdk.api_client import APIClient

class TestContactsIntegration(unittest.TestCase):
    def setUp(self):
        """
        Set up an actual instance of Contacts for integration testing.
        """
        self.client = APIClient(config_path="sdk/config.yaml")
        self.contacts = Contacts(client=self.client)
        self.messages = Messages(client=self.client)

    def test_create_get_update_delete_contact_expects_successful_deletion(self):
        """
        Test creating, getting, updating, and deleting a contact in an integration environment.
        """
        # Create a contact
        name = "Jane Doe"
        phone = "+14155552671"
        created_contact = self.contacts.create_contact(name=name, phone=phone)
        self.assertIn("id", created_contact)
        contact_id = created_contact["id"]

        # Get the contact
        response = self.contacts.get_contact(contact_id=contact_id)
        print("Get Contact Response:", response)
        self.assertEqual(response["id"], contact_id)
        self.assertEqual(response["name"], name)
        self.assertEqual(response["phone"], phone)

        # Update the contact
        new_name = "Jane Smith"
        update_response = self.contacts.update_contact(contact_id=contact_id, name=new_name)
        self.assertEqual(update_response["id"], contact_id)
        self.assertEqual(update_response["name"], new_name)

        # Get the updated contact
        updated_contact = self.contacts.get_contact(contact_id=contact_id)
        self.assertEqual(updated_contact["name"], new_name)

        # Delete the contact
        delete_response = self.contacts.delete_contact(contact_id=contact_id)
        self.assertIsNone(delete_response)

    def test_create_contacts_send_get_messages_delete_contacts_expects_successful_deletion(self):
        """
        Test sending a message and listing all messages.
        """
        alice = self.contacts.create_contact(name="Alice Doe", phone="+14155552671")
        bob = self.contacts.create_contact(name="Bob Doe", phone="+34612345678")
        alice_id = alice["id"]
        alice_phone = alice["phone"]
        bob_id = bob["id"]

        # Send a message to the contact
        message = "Hello, Bob!"
        send_response = self.messages.send_message(recipient_id=bob_id, content=message, sender_phone=alice_phone)
        self.assertIn("id", send_response)
        message_id = send_response["id"]

        get_message_response = self.messages.get_message(message_id=message_id)
        self.assertIn("content", get_message_response)

        delete_response_bob = self.contacts.delete_contact(contact_id=bob_id)
        self.assertIsNone(delete_response_bob)

        delete_response_alice = self.contacts.delete_contact(contact_id=alice_id)
        self.assertIsNone(delete_response_alice)


if __name__ == "__main__":
    unittest.main()