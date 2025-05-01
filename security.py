from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv

# Generate key (run once)
def generate_key():
    key = Fernet.generate_key()
    with open(".env", "a") as f:
        f.write(f"\nENCRYPTION_KEY={key.decode()}\n")
    return key

# Initialize encryption
load_dotenv()
key = os.getenv("ENCRYPTION_KEY").encode()
cipher = Fernet(key)

def encrypt(data: str) -> bytes:
    """Encrypt sensitive data (API keys, tokens)"""
    return cipher.encrypt(data.encode())

def decrypt(encrypted_data: bytes) -> str:
    """Decrypt data for usage"""
    return cipher.decrypt(encrypted_data).decode()