# pip install PyCryptoDome
from Crypto.Cipher import AES as __AES__
from Crypto.Util.Padding import pad, unpad
import base64
import hashlib
import pickle

__copyright__    = 'Copyright (C) 2024 JavaCommons Technologies'
__version__      = '1.4.2'
__license__      = 'MIT'
__author__       = 'JavaCommons Technologies'
__author_email__ = 'javacommmons@gmail.com'
__url__          = 'https://github.com/lang-library/py-jccrypto'
__all__ = ['JcCrypto', 'AES', 'AES128FromString', 'AES256FromString']

def AES128FromString(str):
    sha256 = hashlib.sha256(str.encode())
    digets = sha256.digest()
    upper16 = digets[0:16]
    lower16 = digets[16:]
    return JcCrypto(upper16, lower16)

def AES256FromString(str):
    sha384 = hashlib.sha384(str.encode())
    digets = sha384.digest()
    upper32 = digets[0:32]
    lower16 = digets[32:]
    return JcCrypto(upper32, lower16)

class JcCrypto:
    def __init__(self, key, iv):
        self.cipher = __AES__.new(key, __AES__.MODE_CBC, iv)
        self.decipher = __AES__.new(key, __AES__.MODE_CBC, iv)
    def encode_bytes(self, data):
        encrypted_data = self.cipher.encrypt(pad(data, __AES__.block_size))
        return base64.b64encode(encrypted_data).decode()
    def decode_bytes(self, base64_text):
        encrypted_data = base64.b64decode(base64_text.encode())
        return unpad(self.decipher.decrypt(encrypted_data), __AES__.block_size)
    def encode_text(self, plain_text):
        data = plain_text.encode()
        return self.encode_bytes(data)
    def decode_text(self, base64_text):
        unpadded_data = self.decode_bytes(base64_text)
        return unpadded_data.decode()
    def encode_pickle(self, x, protocol=3):
        data = pickle.dumps(x, protocol=protocol)
        return self.encode_bytes(data)
    def decode_pickle(self, base64_text):
        unpadded_data = self.decode_bytes(base64_text)
        return pickle.loads(unpadded_data)

class AES(JcCrypto):
    def __init__(self, key, iv):
        super().__init__(key, iv)
