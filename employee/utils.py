from cryptography.fernet import Fernet
from django.conf import settings
import base64

# Retrieve the key from settings
key = settings.ENCRYPTION_KEY.encode()
cipher_suite = Fernet(key)

def encrypt(text):
    encoded_text = text.encode('utf-8')
    encrypted_text = cipher_suite.encrypt(encoded_text)
    return base64.urlsafe_b64encode(encrypted_text).decode('utf-8')

def decrypt(text):
    encrypted_text = base64.urlsafe_b64decode(text)
    decrypted_text = cipher_suite.decrypt(encrypted_text)
    return decrypted_text.decode('utf-8')
