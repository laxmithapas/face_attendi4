from cryptography.fernet import Fernet
import os
from config import BASE_DIR

KEY_FILE = os.path.join(BASE_DIR, 'secret.key')

def load_key():
    """Load the encryption key from the current directory or generate it."""
    if not os.path.exists(KEY_FILE):
        generate_key()
    return open(KEY_FILE, "rb").read()

def generate_key():
    """Generates a key and saves it into a file."""
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as key_file:
        key_file.write(key)

def encrypt_data(data):
    """Encrypts bytes data."""
    key = load_key()
    f = Fernet(key)
    return f.encrypt(data)

def decrypt_data(encrypted_data):
    """Decrypts bytes data."""
    key = load_key()
    f = Fernet(key)
    return f.decrypt(encrypted_data)
