import secrets
import string

ALPHABET = string.ascii_letters + string.digits


def create_code() -> str:
    """
    Create a random string of length 8 using ASCII letters and digits.

    Returns:
        str: A random string of length 8.
    """
    """"""
    return ''.join(secrets.choice(ALPHABET) for _ in range(8))
