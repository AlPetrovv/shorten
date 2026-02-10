import secrets
import string

ALPHABET = string.ascii_letters + string.digits


def create_code() -> str:
    return ''.join(secrets.choice(ALPHABET) for _ in range(8))
