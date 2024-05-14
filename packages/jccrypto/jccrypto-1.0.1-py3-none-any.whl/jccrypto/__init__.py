# pip install PyCryptoDome
from Crypto.Cipher import AES
import base64

__package_name__ = 'pycrypto'
__copyright__    = 'Copyright (C) 2024 JavaCommons Technologies'
__version__      = '1.0.1'
__license__      = 'MIT'
__author__       = 'JavaCommons Technologies'
__author_email__ = 'javacommmons@gmail.com'
__url__          = 'https://github.com/lang-library/py-jccrypto'
__all__ = ['JcCrypto']

class JcCrypto:
    def __init__(self, key, iv):
        self.cipher = AES.new(key, AES.MODE_CBC, iv)
        self.decipher = AES.new(key, AES.MODE_CBC, iv)
    def encode(self, plain_text):
        data = plain_text.encode()
        block_size = AES.block_size
        padding_size = block_size - (len(data) % block_size)
        padded_data = data + bytes([padding_size]) * padding_size
        encrypted_data = self.cipher.encrypt(padded_data)
        return base64.b64encode(encrypted_data).decode()
    def decode(self, base64_text):
        encrypted_data = base64.b64decode(base64_text.encode())
        decrypted_data = self.decipher.decrypt(encrypted_data)
        padding_size = decrypted_data[-1]
        unpadded_data = decrypted_data[:-padding_size]
        return unpadded_data.decode()
