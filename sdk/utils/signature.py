import hmac
import hashlib
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