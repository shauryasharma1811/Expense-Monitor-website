from cryptography.fernet import Fernet
import base64
import hashlib
from app.core.config import Settings

settings = Settings()

# Generate a safe 32-byte url-safe key from the configuration
def _get_fernet():
    key = base64.urlsafe_b64encode(hashlib.sha256(settings.ENCRYPTION_KEY.encode()).digest())
    return Fernet(key)

def encrypt_token(token: str) -> str:
    f = _get_fernet()
    return f.encrypt(token.encode()).decode()

def decrypt_token(encrypted_token: str) -> str:
    f = _get_fernet()
    return f.decrypt(encrypted_token.encode()).decode()
