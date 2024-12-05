import time
import logging
from sdk.resources.contacts import Contacts
from sdk.resources.messages import Messages
from sdk.api_client import APIClient

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def delete_all_contacts(contacts: Contacts):
    """
    Deletes all contacts in the system.
    :param contacts: Instance of the Contacts resource.
    """
    try:
        all_contacts = contacts.list_contacts().get("contacts", [])
        if not all_contacts:
            logging.info("No contacts to delete.")
            return

        logging.info(f"Deleting {len(all_contacts)} contacts...")
        for contact in all_contacts:
            contacts.delete_contact(contact["id"])
            logging.info(f"Deleted contact ID: {contact['id']}")
    except Exception as e:
        logging.error(f"An error occurred while deleting contacts: {e}")


def create_contact(contacts: Contacts, name: str, phone: str):
    """
    Creates a contact and logs the result.
    :param contacts: Instance of the Contacts resource.
    :param name: Name of the contact.
    :param phone: Phone number of the contact.
    :return: The created contact details.
    """
    try:
        contact = contacts.create_contact(name=name, phone=phone)
        logging.info(f"Created contact: {contact}")
        return contact
    except Exception as e:
        logging.error(f"An error occurred while creating contact {name}: {e}")
        return None


def main():
    # Initialize the API client
    client = APIClient(config_path="sdk/config.yaml")
    contacts = Contacts(client)
    messages = Messages(client)

    # Step 1: Delete all existing contacts
    delete_all_contacts(contacts)

    # Step 2: Create two new contacts
    alice = create_contact(contacts, name="Alice", phone="+14155552671")
    bob = create_contact(contacts, name="Bob", phone="+34612345678")

    if not alice or not bob:
        logging.error("Failed to create required contacts. Exiting.")
        return

    logging.info(f"Created contacts: Alice (ID: {alice['id']}), Bob (ID: {bob['id']})")

    # Step 3: Send a message from Alice to Bob
    try:
        message = messages.send_message(
            sender_phone=alice["phone"],
            recipient_id=bob["id"],
            content="Hey, Bob! How are you?"
        )
        logging.info(f"Message sent: {message}")

    except Exception as e:
        logging.error(f"An error occurred while sending a message: {e}")
        return

    # Step 4: Wait for the webhook to process
    logging.info("Waiting for the webhook server to process the event...")
    time.sleep(15)

    # Step 5: Fetch and log the updated message status
    try:
        messages_list = messages.list_messages()
        for msg in messages_list.get("messages", []):
            if msg["id"] == message["id"]:
                logging.info(f"Updated message status: {msg}")
                break
    except Exception as e:
        logging.error(f"Failed to fetch updated message status: {e}")

    logging.info("Workflow complete. Check the webhook server logs for the message status update.")


if __name__ == "__main__":
    main()
