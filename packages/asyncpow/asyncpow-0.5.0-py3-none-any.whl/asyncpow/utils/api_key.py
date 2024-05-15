import base64
import binascii
import uuid


def is_valid_api_key(api_key):
    """Check that the API Key is valid

    Args:
        api_key (str): A base64 string

    Returns:
        bool: True or False
    """
    try:
        # Decode the provided API key
        decoded_value = base64.b64decode(api_key.encode()).decode()

        # Split the decoded value into timestamp and UUID
        timestamp = decoded_value[:13]  # Assuming timestamp is 13 digits (milliseconds)
        uuid_str = decoded_value[13:]

        # Check if the timestamp is a valid integer
        int(timestamp)

        # Check if the UUID is valid
        uuid.UUID(uuid_str)

        return True
    except (ValueError, TypeError, binascii.Error, ValueError, IndexError):
        return False
