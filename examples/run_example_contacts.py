import logging
from sdk.api_client import APIClient
from sdk.resources.contacts import Contacts


def configure_logging():
    """
    Configures logging for the application.
    """
    logging.basicConfig(
        level=logging.INFO,  # Set to DEBUG for verbose output
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )


def list_contacts(contacts: Contacts):
    """
    Fetches and displays all contacts.
    :param contacts: Contacts resource instance.
    """
    logging.info("Listing all contacts...")
    try:
        response = contacts.list_contacts()
        all_contacts = response.get("contacts", [])

        if not all_contacts:
            logging.info("No contacts found.")
        else:
            logging.info(f"Retrieved {len(all_contacts)} contact(s):")
            for contact in all_contacts:
                logging.info(contact)
    except Exception as e:
        logging.error(f"Failed to list contacts: {e}")


def create_contact(contacts: Contacts, name: str, phone: str):
    """
    Creates a new contact.
    :param contacts: Contacts resource instance.
    :param name: Name of the new contact.
    :param phone: Phone number of the new contact.
    :return: Created contact details or None on failure.
    """
    logging.info(f"Creating a new contact: {name}, {phone}")
    try:
        contact = contacts.create_contact(name, phone)
        logging.info("Contact created successfully:")
        logging.info(contact)
        return contact
    except Exception as e:
        logging.error(f"Failed to create contact: {e}")
        return None


def get_contact_details(contacts: Contacts, contact_id: str):
    """
    Retrieves details of a specific contact.
    :param contacts: Contacts resource instance.
    :param contact_id: ID of the contact.
    """
    logging.info(f"Fetching details for contact ID {contact_id}")
    try:
        contact = contacts.get_contact(contact_id)
        logging.info("Contact details retrieved successfully:")
        logging.info(contact)
    except Exception as e:
        logging.error(f"Failed to fetch contact details for ID {contact_id}: {e}")


def update_contact(contacts: Contacts, contact_id: str, name: str = None, phone: str = None):
    """
    Updates a contact's details.
    :param contacts: Contacts resource instance.
    :param contact_id: ID of the contact to update.
    :param name: The updated name of the contact.
    :param phone: The updated phone number of the contact.
    """
    logging.info(f"Updating contact ID {contact_id} with data: {{'name': {name}, 'phone': {phone}}}")
    try:
        updated_contact = contacts.update_contact(contact_id, name=name, phone=phone)
        logging.info("Contact updated successfully:")
        logging.info(updated_contact)
    except Exception as e:
        logging.error(f"Failed to update contact ID {contact_id}: {e}")


def delete_contact(contacts: Contacts, contact_id: str):
    """
    Deletes a contact by ID.
    :param contacts: Contacts resource instance.
    :param contact_id: ID of the contact to delete.
    """
    logging.info(f"Deleting contact ID {contact_id}")
    try:
        contacts.delete_contact(contact_id)
        logging.info(f"Contact ID {contact_id} deleted successfully.")
    except Exception as e:
        logging.error(f"Failed to delete contact ID {contact_id}: {e}")


def delete_all_contacts(contacts: Contacts):
    """
    Deletes all contacts in the system.
    :param contacts: Contacts resource instance.
    """
    logging.info("Deleting all contacts...")
    try:
        # Fetch all contacts
        response = contacts.list_contacts()
        all_contacts = response.get("contacts", [])

        if not all_contacts:
            logging.info("No contacts found for deletion.")
            return

        logging.info(f"Found {len(all_contacts)} contact(s). Starting deletion process...")
        for contact in all_contacts:
            contact_id = contact["id"]
            delete_contact(contacts, contact_id)
    except Exception as e:
        logging.error(f"Failed to delete all contacts: {e}")


def main():
    """
    Demonstrates basic usage of the SDK.
    """
    configure_logging()

    # Initialize the API client and resources
    client = APIClient(config_path="sdk/config.yaml")
    contacts = Contacts(client)

    # Delete all existing contacts
    delete_all_contacts(contacts)

    # List contacts after cleanup
    list_contacts(contacts)

    # Create a new contact
    new_contact = create_contact(contacts, "Lucy Doe", "+14155552671")

    if not new_contact:
        return

    contact_id = new_contact["id"]
    get_contact_details(contacts, contact_id)

    # Update the contact's details
    update_contact(contacts, contact_id, name="Lucy Doe Smith", phone="+34612345678")

    # Delete the updated contact
    delete_contact(contacts, contact_id)

    # Confirm deletion
    list_contacts(contacts)


if __name__ == "__main__":
    main()
